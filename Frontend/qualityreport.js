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


        if(!response.ok){

            throw new Error(data.detail);

        }



        if(!data.AI_summary){

            throw new Error("AI summary is empty");

        }



        renderAISummary(
            cleanAIText(data.AI_summary)
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

    <th>Column Name</th>

    <th>Count</th>

    </tr>

    </thead>

    <tbody>

    `;



    for(let column in data){


        html+=`

        <tr>

        <td>${column}</td>

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


    const overallIndex =
    summary.indexOf("Overall Dataset Summary");


    let tablePart = summary;

    let overallPart = "";



    if(overallIndex !== -1){


        tablePart =
        summary.substring(0,overallIndex).trim();



        overallPart =
        summary.substring(overallIndex).trim();


    }



    const regex =
    /Table Name:\s*(.*?)\s*Overall Condition\s*([\s\S]*?)(?=Table Name:|$)/g;



    let match;



    while((match=regex.exec(tablePart))!==null){



        createTableAICard(
            match[1].trim(),
            match[2].trim()
        );


    }




    if(overallPart){


        createOverallSummary(
            overallPart
        );


    }


}







function createTableAICard(tableName,content){


    const card=document.createElement("div");


    card.className="ai-table-card";



    card.innerHTML=`

    <div class="ai-table-header">

        <i class="fa-solid fa-table"></i>

        <h3>${tableName}</h3>

    </div>


    <div class="ai-table-content">

        ${formatText(content)}

    </div>

    `;



    aiContainer.appendChild(card);


}







function createOverallSummary(content){


    content =
    content.replace(
        "Overall Dataset Summary",
        ""
    ).trim();



    const card=document.createElement("div");


    card.className="ai-overall-card";



    card.innerHTML=`

    <div class="ai-overall-header">

        <i class="fa-solid fa-chart-line"></i>

        <h2>Overall Dataset Summary</h2>

    </div>


    <div class="ai-table-content">

        ${formatText(content)}

    </div>

    `;



    aiContainer.appendChild(card);


}







function cleanAIText(text){


    return text

    .replace(/<think>[\s\S]*?<\/think>/g,"")

    .replace(/\r/g,"")

    .replace(/[ \t]+/g," ")

    .replace(/\n\s*\n\s*\n+/g,"\n\n")

    .trim();

}







function formatText(text){


    return text

    .replace(/\n\n+/g,"<br>")

    .replace(/\n/g," ")

    .replace(/Suggestions:/g,
    "<strong>Suggestions:</strong>")

    .replace(/Overall Condition:/g,
    "<strong>Overall Condition:</strong>")

    .replace(/Final Status:/g,
    "<strong>Final Status:</strong>")

    .replace(/•/g,"&#8226;");


}