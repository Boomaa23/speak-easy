import QRCode from "react-qr-code";

const ItemQrCode = ({ link, boxId, mfgNum, desc }) => {

    return (
        <>
        <div className="w-full">
            <div id="printableDiv" className="w-[216px] h-[384px] border-2 border-black m-auto px-3 rounded-xl overflow-hidden">
                <QRCode className="mx-auto w-full" value={link} />
                <p className="text-lg">Box Id: <span className="font-bold">{boxId}</span></p>
                <p className="text-lg">Mfg PN: <span className="font-bold">{mfgNum}</span></p>
                <p className="text-lg">Desc: <span className="font-bold">{desc}</span></p>
            </div>
        </div>
        </>
    );
}

export default ItemQrCode;
