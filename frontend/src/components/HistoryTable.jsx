import { useState } from "react";

const HistoryTable = ({ history }) => {

    const [expanded,setExpanded]=useState(false);

    if(!history || history.length===0){

        return null;

    }

    const displayHistory=expanded

        ? history

        : history.slice(0,5);

    return(

        <div
            style={card}
        >

            <div
                style={header}
            >

                <h2>

                    Training History

                </h2>

                {

                    history.length>5 &&

                    <button

                        style={button}

                        onClick={()=>setExpanded(!expanded)}

                    >

                        {

                            expanded

                            ?

                            "▲ Show Less"

                            :

                            `▼ View All (${history.length})`

                        }

                    </button>

                }

            </div>

            <table style={table}>

                <thead>

                    <tr>

                        <th>#</th>

                        <th>Model</th>

                        <th>Dataset</th>

                        <th>Accuracy</th>

                        <th>Date</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        displayHistory.map((item,index)=>(

                            <tr key={index}>

                                <td>{index+1}</td>

                                <td>{item.model}</td>

                                <td>{item.dataset_name}</td>

                                <td>

                                    <span
                                        style={badge(item.score)}
                                    >

                                        {(item.score*100).toFixed(2)}%

                                    </span>

                                </td>

                                <td>

                                    {

                                        new Date(

                                            item.created_at

                                        ).toLocaleString()

                                    }

                                </td>

                            </tr>

                        ))

                    }

                </tbody>

            </table>

        </div>

    )

}

const card={

    background:"#fff",

    padding:"25px",

    borderRadius:"18px",

    boxShadow:"0 10px 25px rgba(0,0,0,.08)",

}

const header={

    display:"flex",

    justifyContent:"space-between",

    alignItems:"center",

    marginBottom:"20px"

}

const button={

    background:"#2563eb",

    color:"white",

    border:"none",

    padding:"10px 16px",

    borderRadius:"8px",

    cursor:"pointer"

}

const table={

    width:"100%",

    borderCollapse:"collapse"

}

const badge=(score)=>{

    if(score>=0.9){

        return{

            background:"#16a34a",

            color:"white",

            padding:"6px 10px",

            borderRadius:"20px"

        }

    }

    if(score>=0.8){

        return{

            background:"#f59e0b",

            color:"white",

            padding:"6px 10px",

            borderRadius:"20px"

        }

    }

    return{

        background:"#dc2626",

        color:"white",

        padding:"6px 10px",

        borderRadius:"20px"

    }

}

export default HistoryTable;