import './App.css'
import './index.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Landing from "./components/Landing";
import Item from './components/Item';

function App() {
    return (
        <BrowserRouter>
            <Routes basename="/inventory">
                <Route path="/" element={<Landing />} />
                <Route path="/item/:itemId" element={<Item />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
