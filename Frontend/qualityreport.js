const qualityContainer = document.getElementById("quality-container");
const errorMessage = document.getElementById("error-message");
const fileTemplate = document.getElementById("file-template");

const generateBtn = document.getElementById("generate-ai-btn");
const aiLoading = document.getElementById("ai-loading");
const aiContainer = document.getElementById("ai-summary-container");


let qualityId = localStorage.getItem("quality_id");



window.onload = function(){

    loadQualityReport();

};





async function loadQualityReport(){


    if(!qualityId){

        errorMessage.innerText="Quality ID not found";
        return;

    }


    try{


        const response = await fetch(
            `http://127.0.0.1:8000/user/files/qualities/${qualityId}`
        );


        const data = await response.json();


        if(!response.ok){

            errorMessage.innerText=data.detail;
            return;

        }


        renderFiles(data["files quality"]);


    }
    catch(error){

        errorMessage.innerText="Unable to connect with server";

    }


}






generateBtn.addEventListener(
    "click",
    generateAISummary
);







async function generateAISummary(){


    generateBtn.disabled=true;

    aiLoading.style.display="flex";

    aiContainer.innerHTML="";


    try{


        const response = await fetch(
            `http://127.0.0.1:8000/table/aisummary?quality_id=${qualityId}`
        );


        const data = await response.json();



        console.log(data);



        if(!response.ok){

            throw new Error(data.detail);

        }



        if(!data.AI_summary){

            throw new Error("AI summary is empty");

        }



        renderAISummary(
            data.AI_summary
        );



    }
    catch(error){


        aiContainer.innerHTML=`

        <div class="ai-card">

        <p>
        ${error.message}
        </p>

        </div>

        `;


    }
    finally{


        aiLoading.style.display="none";

        generateBtn.disabled=false;


    }


}









function renderFiles(files){


    qualityContainer.innerHTML="";


    files.forEach(file=>{


        const clone =
        fileTemplate.content.cloneNode(true);



        clone.querySelector(".file-name").innerText =
        file["movie name"];



        clone.querySelector(".missing-total").innerText =
        calculateTotal(file["missing values"]);



        clone.querySelector(".empty-total").innerText =
        calculateTotal(file["empty strings"]);



        clone.querySelector(".duplicate-total").innerText =
        file["duplicated rows"];



        clone.querySelector(".missing-table").innerHTML =
        createTable(file["missing values"]);



        clone.querySelector(".empty-table").innerHTML =
        createTable(file["empty strings"]);



        qualityContainer.appendChild(clone);



    });


}









function calculateTotal(data){


    let total=0;


    for(let key in data){

        total += Number(data[key]);

    }


    return total;


}









function createTable(data){


    let html=`

    <table>

    <thead>

    <tr>

    <th>
    Column Name
    </th>

    <th>
    Count
    </th>

    </tr>

    </thead>


    <tbody>

    `;



    for(let column in data){



        html+=`

        <tr>


        <td>
        ${column}
        </td>


        <td>

        <span class="${data[column]==0?'good':'bad'}">

        ${data[column]}

        </span>

        </td>


        </tr>

        `;


    }



    html+=`

    </tbody>

    </table>

    `;


    return html;


}









function renderAISummary(summary){



    aiContainer.innerHTML="";



    summary = summary.replace(
        /<think>[\s\S]*?<\/think>/g,
        ""
    );



    let parts = summary.split("**");



    let overall="";



    for(let i=1;i<parts.length;i+=2){



        let title = parts[i].trim();


        let content = parts[i+1]
        ? parts[i+1].trim()
        : "";



        if(
            title.toLowerCase()
            .includes("overall dataset summary")
        ){


            overall=content;

        }
        else{


            createAISummaryCard(
                title,
                content
            );


        }


    }





    if(overall){


        createOverallCard(overall);


    }



}









function createAISummaryCard(title,content){



    let card=document.createElement("div");


    card.className="ai-card";



    card.innerHTML=`

    <div class="ai-card-header">


    <i class="fa-solid fa-table"></i>


    <h3>
    ${title}
    </h3>


    </div>



    <p>

    ${formatText(content)}

    </p>


    `;



    aiContainer.appendChild(card);



}









function createOverallCard(content){



    let card=document.createElement("div");


    card.className="overall-card";



    card.innerHTML=`

    <div class="overall-title">


    <i class="fa-solid fa-chart-line"></i>


    <h2>
    Overall Dataset Summary
    </h2>


    </div>


    <p>

    ${formatText(content)}

    </p>


    `;



    aiContainer.appendChild(card);



}






function formatText(text){


    return text
    .replace(/\n/g,"<br>")
    .replace(/- /g,"• ");


}