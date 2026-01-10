import React,{ useState } from 'react';
import Tree from 'react-d3-tree';
import { Play,Code2,Terminal,FileJson,AlertCircle } from 'lucide-react'; // Icons
import { ASTNode } from './types';
import { TransformAST,renderCustomNode } from './TransformedNode';
import './App.css';

const INITIAL_CODE = `PRINT "Compiling..."
LET a = 10
LET b = 20
WHILE a > 0 REPEAT
    PRINT a
    LET a = a - 1
ENDWHILE
PRINT "Done!"`;

const SYNTAX_RULES = [
  { cmd: "PRINT",example: 'PRINT "Hello"',desc: "Print text or variables" },
  { cmd: "LET",example: "LET a = 5",desc: "Declare numeric variable" },
  { cmd: "INPUT",example: "INPUT n",desc: "Read user input" },
  { cmd: "IF",example: "IF a > 0 THEN ... ENDIF",desc: "Conditional block" },
  { cmd: "WHILE",example: "WHILE a < 10 REPEAT ... END",desc: "Loop block" },
  { cmd: "Ops",example: "+ - * / > < ==",desc: "Math & Logic" },
];

function App() {
  const [sourceCode,setSourceCode] = useState(INITIAL_CODE);
  const [cOutput,setCOutput] = useState("// Click Run to compile...");
  const [astData,setAstData] = useState<any>(null);
  const [error,setError] = useState("");
  const [loading,setLoading] = useState(false);

  const handleCompile = async () => {
    setLoading(true);
    setError("");
    setAstData(null); // Clear tree for dramatic effect

    const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5050';

    try {
      // Simulate network delay for "processing" feel
      // await new Promise(r => setTimeout(r, 600)); 

      const response = await fetch(`${API_URL}/compile`,{
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: sourceCode })
      });

      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setCOutput("")
      } else {
        setCOutput(data.c_code);
        setAstData(TransformAST(data.ast));
      }
    } catch (err) {
      setError("Failed to connect to compiler server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* HEADER */}
      <header className="navbar">
        <div className="logo">
          <Code2 size={24} color="#61dafb" />
          <span>PyToC <span className="highlight">Compiler</span></span>
        </div>
        <div className="actions">
          <a href="https://github.com/sanketlengare/my-compiler" target="_blank" rel="noreferrer" className="link">GitHub</a>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="workspace">

        {/* LEFT COLUMN: EDITORS */}
        <div className="editor-column">

          {/* INPUT SECTION */}
          <div className="panel input-panel">
            <div className="panel-header">
              <span className="panel-title"><FileJson size={16} /> Source Code</span>
              <button
                className={`run-btn ${loading ? 'loading' : ''}`}
                onClick={handleCompile}
                disabled={loading}
              >
                {loading ? 'Compiling...' : <><Play size={16} fill="currentColor" /> Run Code</>}
              </button>
            </div>
            <div className="editor-wrapper">
              <textarea
                value={sourceCode}
                onChange={(e) => setSourceCode(e.target.value)}
                spellCheck="false"
                placeholder="Write your code here..."
              />
            </div>
          </div>

          {/* OUTPUT SECTION */}
          <div className="panel output-panel">
            <div className="panel-header">
              <span className="panel-title"><Terminal size={16} /> Generated C</span>
            </div>
            <div className="editor-wrapper terminal-wrapper">
              {error ? (
                <div className="error-banner">
                  <AlertCircle size={20} />
                  <span>{error}</span>
                </div>
              ) : null}
              <textarea
                value={cOutput}
                readOnly
                className={error ? "error-text" : "success-text"}
              />
            </div>
          </div>
        </div>



        {/* RIGHT COLUMN: VISUALIZER */}
        <div className="viz-column">
          <div className="panel viz-panel">
            <div className="panel-header">
              <span className="panel-title">Abstract Syntax Tree (AST)</span>
              <span className="badge">Live Visualization</span>
            </div>
            <div className="syntax-card">
              <div className="syntax-header">Syntax Reference</div>
              <div className="syntax-content">
                {SYNTAX_RULES.map((rule,i) => (
                  <div key={i} className="syntax-item">
                    <span className="syntax-cmd">{rule.cmd}</span>
                    <code className="syntax-example">{rule.example}</code>
                  </div>
                ))}
              </div>
            </div>
            <div className="tree-canvas">
              {astData ? (
                <Tree
                  data={astData}
                  orientation="vertical"
                  pathFunc="step"
                  translate={{ x: 400,y: 100 }}
                  renderCustomNodeElement={renderCustomNode}
                  separation={{ siblings: 1,nonSiblings: 1.5 }}
                  nodeSize={{ x: 200,y: 150 }}
                  zoomable={true}
                  pathClassFunc={() => 'tree-link'}
                />
              ) : (
                <div className="empty-state">
                  <Code2 size={64} opacity={0.2} />
                  <p>Ready to Compile</p>
                </div>
              )}
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}

export default App;