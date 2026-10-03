import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import capability_graph_audit as audit


def producer(service_id="producer", event="received.v1", schema="received-v1"):
    return {"id": service_id, "emits": [{"event": event, "schema": schema}], "consumes": []}


def consumer(service_id="consumer", event="received.v1", schema="received-v1", required=True):
    return {"id": service_id, "emits": [], "consumes": [{"event": event, "schema": schema, "required": required}]}


def snapshot(*services):
    return {"format_version": 1, "services": list(services)}


class GraphAuditTests(unittest.TestCase):
    def test_matching_graph(self):
        report = audit.audit_snapshot(snapshot(producer(), consumer()))
        self.assertEqual(report["summary"]["candidate_edges"], 1)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["unconsumed_emissions"], [])

    def test_required_missing_consumer_is_blocking(self):
        report = audit.audit_snapshot(snapshot(consumer()))
        self.assertEqual(report["summary"]["required_waiting"], 1)
        self.assertEqual(report["errors"][0]["reason"], "missing_producer")

    def test_optional_missing_consumer_is_a_warning(self):
        report = audit.audit_snapshot(snapshot(consumer(required=False)))
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["warnings"][0]["code"], "optional_consumer_waiting")

    def test_schema_reference_mismatch_does_not_create_edge(self):
        report = audit.audit_snapshot(snapshot(producer(schema="v2"), consumer()))
        self.assertEqual(report["candidate_edges"], [])
        self.assertEqual(report["errors"][0]["reason"], "schema_reference_mismatch")
        self.assertEqual(report["errors"][0]["available_schema_references"], ["v2"])

    def test_multiple_producers_are_candidates_not_an_automatic_error(self):
        report = audit.audit_snapshot(snapshot(producer("a"), producer("b"), consumer()))
        self.assertEqual(len(report["candidate_edges"]), 2)
        self.assertEqual(report["errors"], [])

    def test_unconsumed_emission_is_not_a_blocking_gap(self):
        report = audit.audit_snapshot(snapshot(producer()))
        self.assertEqual(len(report["unconsumed_emissions"]), 1)
        self.assertEqual(report["errors"], [])

    def test_exact_cycles_do_not_include_a_downstream_tail(self):
        a = producer("a", "a.v1", "a-v1")
        a["consumes"] = consumer(event="b.v1", schema="b-v1")["consumes"]
        b = producer("b", "b.v1", "b-v1")
        b["consumes"] = consumer(event="a.v1", schema="a-v1")["consumes"]
        report = audit.audit_snapshot(snapshot(a, b, consumer("tail", "b.v1", "b-v1")))
        self.assertEqual(report["cyclic_components"], [["a", "b"]])
        self.assertEqual(report["errors"], [])

    def test_self_cycle(self):
        service = producer()
        service["consumes"] = consumer()["consumes"]
        self.assertEqual(audit.audit_snapshot(snapshot(service))["cyclic_components"], [["producer"]])

    def test_long_chain_does_not_recurse(self):
        services = []
        for index in range(1500):
            service = producer(str(index), f"event-{index}", f"schema-{index}")
            if index:
                service["consumes"] = consumer(event=f"event-{index-1}", schema=f"schema-{index-1}")["consumes"]
            services.append(service)
        report = audit.audit_snapshot(snapshot(*services))
        self.assertEqual(report["cyclic_components"], [])
        self.assertEqual(report["summary"]["candidate_edges"], 1499)

    def test_input_validation(self):
        invalid = [snapshot(producer(), producer()), snapshot(consumer(required="true")),
                   {"format_version": True, "services": []}, snapshot({"id": "a", "emits": [], "consumes": [], "policy": {}}),
                   snapshot(producer(event="")), {"format_version": 1, "services": {}}]
        repeated = producer()
        repeated["emits"].append(copy.deepcopy(repeated["emits"][0]))
        invalid.append(snapshot(repeated))
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                audit.validate_snapshot(value)

    def test_duplicate_json_keys_and_non_json_numbers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for value in ('{"format_version":1,"services":[],"services":[]}', '{"format_version":NaN,"services":[]}'):
                path.write_text(value, encoding="utf-8")
                with self.assertRaises(ValueError):
                    audit.load_snapshot(path)

    def test_diff_detects_broken_binding(self):
        previous = audit.audit_snapshot(snapshot(producer(), consumer()))
        current = audit.audit_snapshot(snapshot(producer(event="renamed.v1"), consumer()))
        difference = audit.graph_diff(previous, current)
        self.assertEqual(len(difference["removed_edges"]), 1)
        self.assertEqual(difference["added_edges"], [])
        self.assertEqual(current["summary"]["required_waiting"], 1)

    def test_order_independent_report(self):
        first = snapshot(producer("b"), consumer(), producer("a"))
        second = snapshot(*reversed(first["services"]))
        self.assertEqual(audit.audit_snapshot(first), audit.audit_snapshot(second))

    def test_cli_exit_codes_and_previous_diff(self):
        with tempfile.TemporaryDirectory() as directory:
            path, baseline = Path(directory) / "current.json", Path(directory) / "previous.json"
            baseline.write_text(json.dumps(snapshot(producer(), consumer())), encoding="utf-8")
            for value, expected in [(snapshot(producer(), consumer()), 0), (snapshot(consumer()), 1), ({}, 2)]:
                path.write_text(json.dumps(value), encoding="utf-8")
                stdout, stderr = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    result = audit.main([str(path), "--previous", str(baseline)])
                self.assertEqual(result, expected)
                if expected == 2:
                    self.assertIn("input_error", json.loads(stderr.getvalue()))
                else:
                    self.assertIn("diff", json.loads(stdout.getvalue()))

    def test_missing_file_is_input_error(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(audit.main([str(Path(directory) / "missing.json")]), 2)

    def test_helper_limits_reject_oversized_graphs(self):
        with patch.object(audit, "MAX_SERVICES", 1), self.assertRaises(ValueError):
            audit.audit_snapshot(snapshot(producer(), consumer()))
        with patch.object(audit, "MAX_DECLARATIONS", 1), self.assertRaises(ValueError):
            audit.audit_snapshot(snapshot(producer(), consumer()))
        with patch.object(audit, "MAX_EDGES", 1), self.assertRaises(ValueError):
            audit.audit_snapshot(snapshot(producer("a"), producer("b"), consumer()))

    def test_byte_limit_and_encoding_are_input_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_bytes(b"x" * 9)
            with patch.object(audit, "MAX_BYTES", 8), self.assertRaises(ValueError):
                audit.load_snapshot(path)
            path.write_bytes(b"\xff")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(audit.main([str(path)]), 2)

    def test_empty_graph_is_valid_but_not_runtime_evidence(self):
        report = audit.audit_snapshot(snapshot())
        self.assertEqual(report["scope"], "declared_graph_only")
        self.assertEqual(report["candidate_edges"], [])
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
