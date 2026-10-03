#!/usr/bin/env python3
"""Audit a reduced, declared event graph; no runtime or semantic guarantees."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

MAX_BYTES = 8 * 1024 * 1024
MAX_SERVICES = 20_000
MAX_DECLARATIONS = 100_000
MAX_EDGES = 100_000


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Invalid JSON number: {value}")


def text_field(value, location):
    if not isinstance(value, str) or not value.strip() or len(value) > 1024:
        raise ValueError(f"{location} must be a non-empty string of at most 1024 characters")
    return value


def validate_snapshot(snapshot):
    if not isinstance(snapshot, dict) or set(snapshot) != {"format_version", "services"}:
        raise ValueError("Snapshot must contain only format_version and services")
    if type(snapshot["format_version"]) is not int or snapshot["format_version"] != 1:
        raise ValueError("format_version must be integer 1")
    services = snapshot["services"]
    if not isinstance(services, list) or len(services) > MAX_SERVICES:
        raise ValueError(f"services must be an array with at most {MAX_SERVICES} entries")
    seen_ids = set()
    declaration_count = 0
    for index, service in enumerate(services):
        location = f"services[{index}]"
        if not isinstance(service, dict) or set(service) != {"id", "emits", "consumes"}:
            raise ValueError(f"{location} must contain only id, emits, and consumes")
        service_id = text_field(service["id"], f"{location}.id")
        if service_id in seen_ids:
            raise ValueError(f"Duplicate service id: {service_id}")
        seen_ids.add(service_id)
        for direction in ("emits", "consumes"):
            declarations = service[direction]
            if not isinstance(declarations, list):
                raise ValueError(f"{location}.{direction} must be an array")
            declaration_count += len(declarations)
            if declaration_count > MAX_DECLARATIONS:
                raise ValueError(f"Snapshot exceeds {MAX_DECLARATIONS} event declarations")
            seen_events = set()
            expected = {"event", "schema", "required"} if direction == "consumes" else {"event", "schema"}
            for declaration in declarations:
                if not isinstance(declaration, dict) or set(declaration) != expected:
                    raise ValueError(f"{location}.{direction} entries must contain only {sorted(expected)}")
                event = text_field(declaration["event"], f"{location}.{direction}.event")
                text_field(declaration["schema"], f"{location}.{direction}.schema")
                if event in seen_events:
                    raise ValueError(f"Duplicate {direction} event {event} in {service_id}")
                seen_events.add(event)
                if direction == "consumes" and type(declaration["required"]) is not bool:
                    raise ValueError(f"{location}.consumes.required must be boolean")
    return snapshot


def load_snapshot(path):
    with Path(path).open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"Snapshot exceeds {MAX_BYTES} bytes")
    snapshot = json.loads(data.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)
    return validate_snapshot(snapshot)


def cyclic_components(nodes, adjacency):
    # Iterative Kosaraju traversal avoids recursion limits on long service chains.
    visited = set()
    finished = []
    for start in sorted(nodes):
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, iter(sorted(adjacency[start])))]
        while stack:
            node, neighbors = stack[-1]
            neighbor = next(neighbors, None)
            if neighbor is None:
                finished.append(node)
                stack.pop()
            elif neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, iter(sorted(adjacency[neighbor]))))
    reverse = {node: set() for node in nodes}
    for node, neighbors in adjacency.items():
        for neighbor in neighbors:
            reverse[neighbor].add(node)
    assigned = set()
    cycles = []
    for start in reversed(finished):
        if start in assigned:
            continue
        component = []
        stack = [start]
        assigned.add(start)
        while stack:
            node = stack.pop()
            component.append(node)
            for neighbor in sorted(reverse[node]):
                if neighbor not in assigned:
                    assigned.add(neighbor)
                    stack.append(neighbor)
        if len(component) > 1 or start in adjacency[start]:
            cycles.append(sorted(component))
    return sorted(cycles)


def audit_snapshot(snapshot):
    validate_snapshot(snapshot)
    nodes = {service["id"] for service in snapshot["services"]}
    producers = defaultdict(list)
    producer_schemas = defaultdict(set)
    emitted = set()
    for service in snapshot["services"]:
        for declaration in service["emits"]:
            event, schema = declaration["event"], declaration["schema"]
            producers[(event, schema)].append(service["id"])
            producer_schemas[event].add(schema)
            emitted.add((service["id"], event, schema))

    edges = []
    waiting = []
    used_emissions = set()
    adjacency = {node: set() for node in nodes}
    for service in sorted(snapshot["services"], key=lambda item: item["id"]):
        for declaration in sorted(service["consumes"], key=lambda item: item["event"]):
            event, schema = declaration["event"], declaration["schema"]
            matches = producers.get((event, schema), [])
            if not matches:
                waiting.append({
                    "service": service["id"], "event": event, "schema": schema,
                    "required": declaration["required"],
                    "reason": "schema_reference_mismatch" if event in producer_schemas else "missing_producer",
                    "available_schema_references": sorted(producer_schemas.get(event, set())),
                })
            for producer in sorted(matches):
                if len(edges) >= MAX_EDGES:
                    raise ValueError(f"Graph exceeds {MAX_EDGES} candidate edges; use a larger graph tool")
                edges.append({"from": producer, "event": event, "schema": schema, "to": service["id"]})
                used_emissions.add((producer, event, schema))
                adjacency[producer].add(service["id"])

    edges.sort(key=lambda edge: (edge["from"], edge["event"], edge["schema"], edge["to"]))
    cycles = cyclic_components(nodes, adjacency)
    unconsumed = [
        {"service": service, "event": event, "schema": schema}
        for service, event, schema in sorted(emitted - used_emissions)
    ]
    errors = [{"code": "required_consumer_waiting", **item} for item in waiting if item["required"]]
    warnings = [{"code": "optional_consumer_waiting", **item} for item in waiting if not item["required"]]
    warnings.extend({"code": "cycle_requires_review", "services": component} for component in cycles)
    return {
        "scope": "declared_graph_only",
        "services": sorted(nodes), "candidate_edges": edges,
        "waiting_consumers": waiting, "unconsumed_emissions": unconsumed,
        "cyclic_components": cycles, "errors": errors, "warnings": warnings,
        "summary": {"services": len(nodes), "candidate_edges": len(edges),
                    "required_waiting": len(errors), "warnings": len(warnings)},
    }


def graph_diff(previous, current):
    old_nodes, new_nodes = set(previous["services"]), set(current["services"])
    def edge_keys(report):
        return {(edge["from"], edge["event"], edge["schema"], edge["to"]) for edge in report["candidate_edges"]}
    def edge_records(keys):
        return [{"from": source, "event": event, "schema": schema, "to": target}
                for source, event, schema, target in sorted(keys)]
    old_edges, new_edges = edge_keys(previous), edge_keys(current)
    return {"added_services": sorted(new_nodes - old_nodes), "removed_services": sorted(old_nodes - new_nodes),
            "added_edges": edge_records(new_edges - old_edges), "removed_edges": edge_records(old_edges - new_edges)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--previous", type=Path, help="Compare with an earlier reduced snapshot")
    args = parser.parse_args(argv)
    try:
        report = audit_snapshot(load_snapshot(args.snapshot))
        if args.previous is not None:
            report["diff"] = graph_diff(audit_snapshot(load_snapshot(args.previous)), report)
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        print(json.dumps({"scope": "declared_graph_only", "input_error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
