import { useState, useCallback, useEffect } from 'react';
import { AgGridReact } from 'ag-grid-react';
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-quartz.css";
import Modal from 'react-modal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons'

const Table = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleOpenModal = () => {
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const [newDescription, setNewDescription] = useState('');
    const [newBoxID, setNewBoxID] = useState('');
    const [newQuantity, setNewQuantity] = useState('');
    const [newMfgPN, setNewMfgPN] = useState('');
    const [newDigikeyPN, setNewDigikeyPN] = useState('');
    const [newMouserPN, setNewMouserPN] = useState('');
    const [newJlcpcbPN, setNewJlcpcbPN] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();

        const formdata = new FormData();
        formdata.append("box_id", newBoxID);
        formdata.append("mfg_part_number", newMfgPN);
        formdata.append("quantity", newQuantity);
        formdata.append("description", newDescription);
        formdata.append("digikey_part_number", newDigikeyPN);
        formdata.append("mouser_part_number", newMouserPN);
        formdata.append("jlcpcb_part_number", newJlcpcbPN);
        formdata.append("api_key", "636e0c5c873afcef9a6fa5996edc9c8da49891b7b1ffbdb1720221ccf1e0e184");

        const requestOptions = {
            method: "POST",
            body: formdata,
            redirect: "follow"
        };

        fetch(`${window.env.REACT_APP_API_URL}/api/item/create`, requestOptions).then((response) => {
            if (!response.ok) { alert(response.statusText) } else { window.location.href = '/' }
        })
    }

    const [colDefs] = useState([
        { headerName: "Description", field: "description", flex: 1 },
        { headerName: "Box ID", field: "box_id", flex: 0.7 },
        { headerName: "Quantity", field: "quantity", flex: 0.5 },
        { headerName: "Manufacturer Part Number", field: "mfg_part_number", flex: 1 },
        { headerName: "DigiKey Part Number", field: "digikey_part_number", flex: 1 },
        { headerName: "JLCPCB Part Number", field: "jlcpcb_part_number", flex: 1 },
        { headerName: "Mouser Part Number", field: "mouser_part_number", flex: 1 },
    ]);

    const [rowData, setRowData] = useState([]);

    useEffect(() => {
        const fetchParts = async () => {
            try {
                const response = await fetch(`${window.env.REACT_APP_API_URL}/api/items/list`);

                if (!response.ok) {
                    throw new Error('Network response failure');
                }

                const data = await response.json();
                setRowData(data.body);
            } catch (error) {
                console.error(error.message);
            }
        };

        fetchParts();
    }, []);

    const [quickFilterText, setQuickFilterText] = useState();
    const onFilterTextBoxChanged = useCallback(
        ({ target: { value } }) =>
            setQuickFilterText(value),
        []
    );

    const routeToItemPage = (params) => {
        window.location.href = `/item/${params.data.item_id}`;
    }

    return (
        <div>
            <div className='flex justify-end mb-7 items-center'>
                <input
                    type="text"
                    id="filter-text-box"
                    placeholder="Search Inventory..."
                    onInput={onFilterTextBoxChanged}
                    className='w-full border-2 border-black text-left py-2 px-5 rounded-full'
                />

                <button className='flex items-center border-black border-2 rounded-full ml-4 p-1 hover:bg-gray-300 transition' onClick={handleOpenModal}>
                    <FontAwesomeIcon className='size-6' icon={faPlus} />
                </button>
            </div>

            <Modal
                isOpen={isModalOpen}
                onRequestClose={handleCloseModal}
                contentLabel="Add Item Modal"
                ariaHideApp={false}
                style={{
                    overlay: {
                        display: 'flex',
                        justifyContent: 'center'
                    },
                    content: {
                        borderRadius: '15px',
                        display: 'flex',
                        width: '384px',
                        height: '384px',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                    }
                }}
            >
                <div className='w-full'>
                    <h1 className='text-xl font-semibold'>Add Item to Inventory</h1>
                    <form className='w-full' onSubmit={handleSubmit}>
                        <hr className='my-3' />
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>Description:</label>
                            <input value={newDescription} onChange={(event) => setNewDescription(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>Box ID:</label>
                            <input value={newBoxID} onChange={(event) => setNewBoxID(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>Quantity:</label>
                            <input value={newQuantity} onChange={(event) => setNewQuantity(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>Manufacturer PN:</label>
                            <input value={newMfgPN} onChange={(event) => setNewMfgPN(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>DigiKey PN:</label>
                            <input value={newDigikeyPN} onChange={(event) => setNewDigikeyPN(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>Mouser PN:</label>
                            <input value={newMouserPN} onChange={(event) => setNewMouserPN(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <div className='flex item-center my-2'>
                            <label className='shrink-0'>JLCPCB PN:</label>
                            <input value={newJlcpcbPN} onChange={(event) => setNewJlcpcbPN(event.target.value)} className='grow bg-gray-100 border-black border rounded-md ml-2 px-1' type="text" />
                        </div>
                        <hr className='my-3' />
                        <button className='float-right bg-red-300 py-1 px-3 rounded-md hover:bg-red-500 transition' onClick={handleCloseModal}>Close</button>
                        <button type='submit' className='float-right bg-gray-300 py-1 px-3 rounded-md hover:bg-green-500 mx-2 transition'>Submit</button>
                    </form>
                </div>
            </Modal >

            <div className="ag-theme-quartz w-full h-[60vh]">
                <AgGridReact
                    className='w-full'
                    rowData={rowData}
                    columnDefs={colDefs}
                    quickFilterText={quickFilterText}
                    onRowClicked={routeToItemPage}
                />
            </div>
            <div className='w-100 flex justify-end mt-2'>
                <p>
                    # of Items: {rowData.length}
                </p>
            </div>
        </div >
    );
};

export default Table;
