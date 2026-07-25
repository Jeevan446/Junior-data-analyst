const qualityContainer = document.getElementById("quality-container");
const errorMessage = document.getElementById("error-message");
const fileTemplate = document.getElementById("file-template");


window.onload = function () {
    loadQualityReport();
};



async function loadQualityReport() {

    const quality_id = localStorage.getItem("quality_id");


    if (!quality_id) {

        errorMessage.innerText = "Quality ID not found";
        return;

    }


    try {


        const response = await fetch(
            `http://127.0.0.1:8000/user/files/qualities/${quality_id}`
        );


        const data = await response.json();


        if (!response.ok) {

            errorMessage.innerText = data.detail;
            return;

        }


        renderFiles(data["files quality"]);


    }
    catch(error){

        console.log(error);

        errorMessage.innerText =
            "Unable to connect with server";

    }

}





function renderFiles(files){


    qualityContainer.innerHTML="";


    files.forEach(file=>{


        const clone =
        fileTemplate.content.cloneNode(true);



        const fileName =
        clone.querySelector(".file-name");


        fileName.innerText =
        file["movie name"];




        const missingTotal =
        calculateTotal(file["missing values"]);



        const emptyTotal =
        calculateTotal(file["empty strings"]);




        clone.querySelector(".missing-total")
        .innerText = missingTotal;



        clone.querySelector(".empty-total")
        .innerText = emptyTotal;



        clone.querySelector(".duplicate-total")
        .innerText =
        file["duplicated rows"];





        clone.querySelector(".missing-table")
        .innerHTML =
        createTable(file["missing values"]);




        clone.querySelector(".empty-table")
        .innerHTML =
        createTable(file["empty strings"]);




        qualityContainer.appendChild(clone);


    });


}





function calculateTotal(data){


    let total = 0;


    for(let key in data){

        total += Number(data[key]);

    }


    return total;

}





function createTable(data){


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



    for(let column in data){


        let value = data[column];


        html += `

            <tr>

                <td>
                    ${column}
                </td>


                <td>

                    <span class="${value == 0 ? "good" : "bad"}">

                        ${value}

                    </span>

                </td>


            </tr>

        `;


    }



    html += `

            </tbody>

        </table>

    `;


    return html;

}