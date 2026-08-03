const qualityContainer = document.getElementById("quality-container");
const errorMessage = document.getElementById("error-message");
const fileTemplate = document.getElementById("file-template");

const generateBtn = document.getElementById("generate-ai-btn");
const aiLoading = document.getElementById("ai-loading");
const aiContainer = document.getElementById("ai-summary-container");


let qualityId = localStorage.getItem("quality_id");



window.onload = function () {

    loadQualityReport();

};




// ===============================
// LOAD QUALITY REPORT
// ===============================


async function loadQualityReport() {


    if (!qualityId) {

        errorMessage.innerText = "Quality ID not found";
        return;

    }


    try {


        const response = await fetch(
            `http://127.0.0.1:8000/user/files/qualities/${qualityId}`
        );


        const data = await response.json();


        if(!response.ok){

            errorMessage.innerText =
                data.detail || "Failed to load report";

            return;

        }



        renderFiles(
            data["files quality"]
        );


    }
    catch(error){

        errorMessage.innerText =
            "Unable to connect with server";

    }

}






// ===============================
// GENERATE AI SUMMARY
// ===============================


generateBtn.addEventListener(
    "click",
    generateAISummary
);





async function generateAISummary(){


    generateBtn.disabled = true;

    aiLoading.style.display = "flex";

    aiContainer.innerHTML = "";



    try{


        const response = await fetch(

            `http://127.0.0.1:8000/table/aisummary?quality_id=${qualityId}`

        );



        const data = await response.json();



        console.log(
            "BACKEND RESPONSE:",
            data
        );



        if(!response.ok){

            throw new Error(
                data.detail || "AI generation failed"
            );

        }



        let report = data;



        // remove wrapper
        if(report.AI_summary){

            report = report.AI_summary;

        }



        // if AI_summary is string JSON
        if(typeof report === "string"){


            report = cleanAIText(report);


            report = JSON.parse(report);


        }



        // handle nested AI_summary
        while(report.AI_summary){

            report = report.AI_summary;

        }



        console.log(
            "FINAL REPORT:",
            report
        );



        renderAISummary(report);



    }
    catch(error){


        console.log(error);


        aiContainer.innerHTML = `

        <div class="ai-card">

            <p>
                ${error.message}
            </p>

        </div>

        `;


    }
    finally{


        aiLoading.style.display = "none";

        generateBtn.disabled = false;


    }

}









// ===============================
// DISPLAY FILE QUALITY
// ===============================


function renderFiles(files){


    qualityContainer.innerHTML = "";



    if(!Array.isArray(files)){

        return;

    }



    files.forEach(file=>{


        const clone =
            fileTemplate.content.cloneNode(true);



        clone.querySelector(".file-name").innerText =
            file["movie name"] || "Unknown";



        clone.querySelector(".missing-total").innerText =
            calculateTotal(
                file["missing values"]
            );



        clone.querySelector(".empty-total").innerText =
            calculateTotal(
                file["empty strings"]
            );



        clone.querySelector(".duplicate-total").innerText =
            file["duplicated rows"] || 0;



        clone.querySelector(".missing-table").innerHTML =
            createTable(
                file["missing values"]
            );



        clone.querySelector(".empty-table").innerHTML =
            createTable(
                file["empty strings"]
            );



        qualityContainer.appendChild(clone);


    });


}








function calculateTotal(data){


    let total = 0;


    if(!data){

        return 0;

    }



    Object.values(data).forEach(value=>{

        total += Number(value);

    });



    return total;


}








function createTable(data){


    if(!data){

        return "";

    }


    let html = `

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



    Object.keys(data).forEach(column=>{


        html += `


        <tr>


        <td>
        ${column}
        </td>


        <td>

        <span class="${
            data[column]==0
            ?
            "good"
            :
            "bad"
        }">

        ${data[column]}

        </span>


        </td>


        </tr>


        `;


    });



    html += `

    </tbody>

    </table>

    `;



    return html;

}









// ===============================
// AI REPORT DISPLAY
// ===============================


function renderAISummary(report){


    aiContainer.innerHTML = "";



    if(
        !report ||
        !Array.isArray(report.tables)
    ){


        console.log(
            "INVALID REPORT:",
            report
        );


        aiContainer.innerHTML = `

        <div class="ai-card">

        <p>
        Invalid AI report format
        </p>

        </div>

        `;


        return;


    }




    report.tables.forEach(table=>{


        createTableAICard(table);


    });




    if(report.overall_dataset_summary){


        createOverallSummary(
            report.overall_dataset_summary
        );


    }



}









function createTableAICard(table){



    const card =
        document.createElement("div");



    card.className =
        "ai-table-card";



    card.innerHTML = `


    <div class="ai-table-header">


    <i class="fa-solid fa-table"></i>


    <h3>
    ${table.table_name}
    </h3>


    </div>




    <div class="ai-table-content">



    <h4>
    Overall Condition
    </h4>


    <p>
    ${table.overall_condition}
    </p>





    <h4>
    Suggestions
    </h4>



    <ul>


    ${
        (table.suggestions || [])
        .map(item=>`

        <li>
        ${item}
        </li>

        `)
        .join("")
    }


    </ul>





    <h4>
    Final Status
    </h4>


    <p class="status">

    ${table.final_status}

    </p>



    </div>


    `;



    aiContainer.appendChild(card);


}









function createOverallSummary(summary){


    const card =
        document.createElement("div");



    card.className =
        "ai-overall-card";



    card.innerHTML = `


<div class="ai-overall-header">

<i class="fa-solid fa-chart-line"></i>

<h2>
Overall Dataset Summary
</h2>

</div>



<div class="ai-table-content">


<h4>
Quality Summary
</h4>

<p>
${summary.quality_summary}
</p>



<h4>
Important Information
</h4>

<p>
${summary.important_information}
</p>



<h4>
Duplicate Records
</h4>

<p>
${summary.duplicate_record_summary}
</p>



<h4>
Strengths
</h4>

<p>
${summary.strengths}
</p>



<h4>
Weaknesses
</h4>

<p>
${summary.weaknesses}
</p>



<h4>
Recommended Improvements
</h4>


<ul>


${
(summary.recommended_improvements || [])
.map(item=>`

<li>
${item}
</li>

`)
.join("")
}


</ul>



<h4>
Business Usage
</h4>


<p>
<b>Reports:</b>
${summary.business_usage?.reports || ""}
</p>


<p>
<b>Dashboards:</b>
${summary.business_usage?.dashboards || ""}
</p>


<p>
<b>Business Decisions:</b>
${summary.business_usage?.business_decisions || ""}
</p>


<p>
<b>Further Analysis:</b>
${summary.business_usage?.further_analysis || ""}
</p>


<p>
<b>Machine Learning:</b>
${summary.business_usage?.machine_learning || ""}
</p>


<p>
<b>Prediction Models:</b>
${summary.business_usage?.prediction_models || ""}
</p>



<h4>
Trust Level
</h4>


<p>
${summary.trust_level}
</p>



</div>


`;



    aiContainer.appendChild(card);


}








function cleanAIText(text){


    return text

    .replace(/<think>[\s\S]*?<\/think>/g,"")

    .replace(/```json/g,"")

    .replace(/```/g,"")

    .replace(/\r/g,"")

    .trim();


}