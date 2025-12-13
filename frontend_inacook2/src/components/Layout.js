import React from 'react';
import Header from './Header';

export default function Layout({children}){
  return (
    <div>
      <Header />
      <div className="content">
        <div className="container">{children}</div>
      </div>
    </div>
  );
}
