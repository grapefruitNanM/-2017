import React from 'react';
import { Header, Navbar } from 'rsuite';
import 'main.less';
import { render } from 'react-dom';

const App = ()=>{
    return (
        <div className="doc-page">
            <Header inverse>
                <div className="container">
                    <Navbar.Header>
                        <Navbar.Brand>
                            <a href="#"><span className="prefix">R</span>Suite</a>
                        </Navbar.Brand>
                        <Navbar.Toggle />
                    </Navbar.Header>

                </div>
            </Header>

            <div className="container">
                <h1 className="page-header">
                    Hello Word!
                </h1>
                <Home/>
            </div>
        </div>
    )
}
render(App, document.getElementById('root'));
