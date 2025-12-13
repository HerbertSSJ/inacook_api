import React, { useState } from 'react';
export default function Calculadora(){
  const [expr, setExpr] = useState('');
  const [res, setRes] = useState('');
  function calcular(){ try{ setRes(eval(expr)); }catch{ setRes('Error'); } }
  return (
    <div className="page calculadora">
      <h1>Calculadora</h1>
      <div className="calculadora-container">
        <div className="calculadora container">
          <input className="display" value={expr} onChange={e=>setExpr(e.target.value)} />
          <div className="buttons">
            <button className="btn" onClick={calcular}>Calcular</button>
          </div>
          <div className="container">Resultado: {String(res)}</div>
        </div>
      </div>
    </div>
  );
}
