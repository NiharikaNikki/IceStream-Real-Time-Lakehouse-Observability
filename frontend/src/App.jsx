import { useCallback, useEffect, useState } from "react";

import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";
import "./App.css";

import { getMetrics } from "./api";


const initialNodes = [
  {
    id: "generator",
    position: { x: 50, y: 180 },
    data: {
      label: "🐍 Python Generator",
    },
    style: {
      padding: 15,
      border: "2px solid #333",
      borderRadius: 10,
      background: "#fff",
      fontWeight: "bold",
    },
  },

  {
    id: "kafka",
    position: { x: 300, y: 180 },
    data: {
      label: "📨 Apache Kafka",
    },
    style: {
      padding: 15,
      border: "2px solid #333",
      borderRadius: 10,
      background: "#fff",
      fontWeight: "bold",
    },
  },

  {
    id: "flink",
    position: { x: 550, y: 180 },
    data: {
      label: "⚡ Apache Flink",
    },
    style: {
      padding: 15,
      border: "2px solid #333",
      borderRadius: 10,
      background: "#fff",
      fontWeight: "bold",
    },
  },

  {
    id: "quality",
    position: { x: 800, y: 180 },
    data: {
      label: "🔍 Data Quality",
    },
    style: {
      padding: 15,
      border: "2px solid #333",
      borderRadius: 10,
      background: "#fff",
      fontWeight: "bold",
    },
  },

  {
    id: "iceberg",
    position: { x: 1050, y: 100 },
    data: {
      label: "🧊 Iceberg Main",
    },
    style: {
      padding: 15,
      border: "2px solid #333",
      borderRadius: 10,
      background: "#fff",
      fontWeight: "bold",
    },
  },

  {
    id: "dlq",
    position: { x: 1050, y: 300 },
    data: {
      label: "🚨 DLQ / Quarantine",
    },
    style: {
      padding: 15,
      border: "2px solid #333",
      borderRadius: 10,
      background: "#fff",
      fontWeight: "bold",
    },
  },
];


const initialEdges = [
  {
    id: "e-generator-kafka",
    source: "generator",
    target: "kafka",
    animated: true,
  },

  {
    id: "e-kafka-flink",
    source: "kafka",
    target: "flink",
    animated: true,
  },

  {
    id: "e-flink-quality",
    source: "flink",
    target: "quality",
    animated: true,
  },

  {
    id: "e-quality-iceberg",
    source: "quality",
    target: "iceberg",
    animated: true,
  },

  {
    id: "e-quality-dlq",
    source: "quality",
    target: "dlq",
    animated: true,
  },
];


function App() {
  const [nodes, setNodes, onNodesChange] =
    useNodesState(initialNodes);

  const [edges, setEdges, onEdgesChange] =
    useEdgesState(initialEdges);


  const [metrics, setMetrics] = useState({
    total_records: 0,
    valid_records: 0,
    invalid_records: 0,
    error_rate: 0,
    dlq_count: 0,
    circuit_state: "CLOSED",
  });


  const [backendStatus, setBackendStatus] = useState(
    "Connecting..."
  );


  const onConnect = useCallback(
    (connection) => {
      setEdges((currentEdges) =>
        addEdge(connection, currentEdges)
      );
    },
    [setEdges]
  );


  useEffect(() => {
    async function loadMetrics() {
      try {
        const data = await getMetrics();

        setMetrics(data);

        setBackendStatus("Connected");
      } catch (error) {
        console.error("Metrics error:", error);

        setBackendStatus("Backend Offline");
      }
    }

    loadMetrics();
  }, []);


  const circuitIsOpen =
    metrics.circuit_state === "OPEN";


  return (
    <div className="dashboard">

      {/* HEADER */}

      <header className="header">

        <div>
          <h1>IceStream</h1>

          <p>
            Real-Time Lakehouse Observability
          </p>
        </div>


        <div className="status">

          <span
            className="status-dot"
            style={{
              background:
                circuitIsOpen
                  ? "red"
                  : backendStatus === "Connected"
                    ? "green"
                    : "orange",
            }}
          ></span>

          Pipeline Status:{" "}

          {circuitIsOpen
            ? "CIRCUIT OPEN"
            : metrics.circuit_state}

        </div>

      </header>


      {/* BACKEND CONNECTION */}

      <div className="backend-status">

        Backend:

        <strong>
          {" "}
          {backendStatus}
        </strong>

      </div>


      {/* METRICS */}

      <section className="metrics">


        <div className="metric-card">

          <h3>Total Records</h3>

          <p>
            {metrics.total_records}
          </p>

        </div>


        <div className="metric-card">

          <h3>Valid Records</h3>

          <p>
            {metrics.valid_records}
          </p>

        </div>


        <div className="metric-card">

          <h3>Invalid Records</h3>

          <p>
            {metrics.invalid_records}
          </p>

        </div>


        <div className="metric-card">

          <h3>Error Rate</h3>

          <p>
            {metrics.error_rate}%
          </p>

        </div>


        <div className="metric-card">

          <h3>DLQ Count</h3>

          <p>
            {metrics.dlq_count}
          </p>

        </div>


      </section>


      {/* CIRCUIT BREAKER STATUS */}

      <section className="circuit-card">

        <h2>
          Circuit Breaker
        </h2>

        <div
          className={
            circuitIsOpen
              ? "circuit-open"
              : "circuit-closed"
          }
        >

          {metrics.circuit_state}

        </div>

        <p>
          Threshold: 2% error rate
        </p>

      </section>


      {/* PIPELINE */}

      <section className="flow-container">

        <h2>
          Live Pipeline Lineage
        </h2>


        <p className="flow-description">
          Real-time data flow from event generation
          through Kafka, Flink, data quality validation,
          and Iceberg storage.
        </p>


        <div className="flow">

          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
          >

            <Background />

            <Controls />

            <MiniMap />

          </ReactFlow>

        </div>

      </section>


      {/* FOOTER */}

      <footer>

        <p>
          IceStream • Real-Time Lakehouse
          Observability Platform
        </p>

      </footer>

    </div>
  );
}


export default App;