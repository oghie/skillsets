# Architecture Style Catalog

Use styles as reusable structural ideas. Most systems combine styles, so evaluate forces, compose deliberately, and rename generic style roles into domain-specific elements.

## Selection Workflow

1. Identify forces: data flow, shared state, UI separation, distribution, scaling, integration, autonomy, control, extensibility, operations, and NFRs.
2. Shortlist styles that match the dominant forces.
3. Evaluate liabilities: coupling, latency, deployment burden, testing complexity, data ownership, governance, observability, and team fit.
4. Integrate selected styles into one schematic architecture.
5. Refine generic elements into domain terms and validate against key scenarios.
6. Add dependency, data-access, policy, or operational fitness checks when a style introduces enforceable constraints.

## Data-Flow Styles

| Style | Use When | Watch For |
|---|---|---|
| Batch Sequential | Work is processed in ordered offline stages | Long feedback cycles, poor interactive fit, restart/recovery |
| Pipe-and-Filter | Data transformations can be staged and composed | Schema drift, error routing, backpressure, ordering |
| Pipeline With Fan-Out/Fan-In | Parallel transformations or enrichment are needed | Aggregation complexity, partial failure, cost |

## Data-Sharing Styles

| Style | Use When | Watch For |
|---|---|---|
| Shared Repository | Many components need a common authoritative data store | Tight schema coupling, unclear write ownership |
| Active Repository | Repository triggers notifications or behavior | Hidden control flow, transactional side effects |
| Blackboard | Multiple knowledge sources incrementally solve a problem | Coordination logic, explainability, convergence |

## Layered And UI Separation Styles

| Style | Use When | Watch For |
|---|---|---|
| Layered | Dependency direction, abstraction, and replaceability matter | Anemic pass-through layers, cross-layer shortcuts |
| Model-View-Controller (MVC) | UI, user interaction, and domain state need separation | Controller bloat, view-model confusion |
| Model-View-Presenter (MVP) | Presenter mediates view logic for testable UI | Presenter complexity, view contract sprawl |
| Model-View-ViewModel (MVVM) | Data binding and view state modeling are central | State synchronization bugs |
| Model-View-Presenter-ViewModel (MVPVM) | UI platform needs both presenter orchestration and view models | Over-abstraction |
| Hierarchical-Model-View-Controller (HMVC) | Complex UI is decomposed into hierarchical modules | Coordination overhead |
| Model-View-Adapter (MVA) | Adapters isolate domain/application from specific interfaces | Adapter proliferation |
| Presentation-Abstraction-Control (PAC) | Complex interactive systems need independent presentation, abstraction, and control agents | Agent coordination and communication overhead |

## Distributed And Coordination Styles

| Style | Use When | Watch For |
|---|---|---|
| Client-Server | Central service provides capabilities to clients | Server bottleneck, offline behavior, versioning |
| N-Tier | Physical/runtime separation of presentation, application, and data is required | Network latency, transaction boundaries |
| Peer-to-Peer | Nodes are symmetric and decentralized | Discovery, consistency, security, operations |
| Broker | Components communicate through a mediator | Broker availability, routing rules, protocol lock-in |
| Dispatcher | Requests must be routed to handlers or workers | Routing policy, observability, overload behavior |
| Master-Slave | A coordinator distributes work to replicas/workers | Coordinator failure, split brain, worker heterogeneity |
| Edge | Work must run near users, devices, or data sources | Deployment sprawl, synchronization, observability |

## Event And Control Styles

| Style | Use When | Watch For |
|---|---|---|
| Event-Driven | Producers and consumers should be decoupled in time or ownership | Ordering, idempotency, schema evolution, tracing |
| Publisher-Subscriber | Many consumers react to topic-based events | Subscription governance, replay, consumer failure |
| Sensor-Controller-Actuator | System senses environment, decides, and acts on physical or runtime targets | Timing, safety, feedback stability, sensor trust |
| Scheduler/Timed Control | Work is triggered by time windows or periodic cycles | Clock drift, overlap, missed runs, recovery |

## Service And Cloud Styles

| Style | Use When | Watch For |
|---|---|---|
| Service-Oriented Architecture | Enterprise capabilities need governed service contracts | Governance overhead, coarse service ownership |
| Microservices | Independent deployability, team autonomy, or scale isolation justifies distribution | Data ownership, distributed transactions, ops cost |
| Serverless | Event-triggered workloads benefit from managed scaling and low ops | Cold starts, limits, vendor coupling, observability |
| Representational State Transfer (REST) | Resource-style APIs and stateless request/response fit | Chatty APIs, weak domain boundaries |
| Space-Based | In-memory distributed state reduces database contention | Consistency, operational complexity, recovery |

For microservices pattern selection, decomposition, sagas, outbox, CQRS, API composition, API gateway/BFF, service mesh, strangler, and coding readiness, use `microservices-pattern-language.md`.

## Adaptability And Plugin Styles

| Style | Use When | Watch For |
|---|---|---|
| Monolithic | Scope is cohesive, team is small, and one deployable keeps delivery simple | Growth into tangled modules, slow releases |
| Modular Monolith | Strong module boundaries are needed without distributed deployment cost | Boundary erosion, hidden shared database coupling |
| Microkernel | Core system must support plugins or product variants | Plugin contracts, security sandboxing, versioning |
| Plug-In Architecture | Optional capabilities can be added independently | Compatibility matrix, lifecycle management |
| Reflective Architecture | System behavior must adapt by inspecting/modifying metadata | Debuggability, safety, performance |
| Whiteboard | Components dynamically register capabilities for discovery | Runtime dependency ambiguity |

## Style Combination Examples

| System Force | Likely Combination |
|---|---|
| Transactional web app | Layered + MVC/MVVM + N-tier + shared repository |
| Data processing platform | Pipe-filter + batch sequential + event-driven + repository |
| Enterprise integration | SOA + broker + pub-sub + layered |
| IoT/control system | Edge + sensor-controller-actuator + event-driven |
| Extensible product platform | Microkernel + plugin + layered + repository |
| Large autonomous teams | Domain-aligned services + event-driven + API gateway/broker |

## Style Instantiation Rules

When composing styles:
- instantiate each style with domain-specific component names before combining it with other styles;
- preserve the style's essential structural property, such as layer direction, pipe/filter ordering, broker mediation, event decoupling, or plugin/core separation;
- define connector semantics: sync/async, protocol, ownership, failure behavior, retries, ordering, security, and observability;
- state which style governs each part of the schematic architecture;
- document conflicts between styles, such as layered shortcuts introduced by event handlers or shared repositories introduced into microservices.

## Rejection Guidance

Reject or defer a style when:
- Its benefits are speculative.
- The team lacks operational capacity.
- Data ownership becomes unclear.
- It introduces distributed failure modes without compensating value.
- It requires NFRs the product does not actually need.
- A simpler style satisfies the same scenarios.
