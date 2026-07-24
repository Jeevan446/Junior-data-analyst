const allFiles = document.getElementById("all-files");
const selectedFilesContainer = document.getElementById("selected-files");
const dropArea = document.getElementById("drop-area");
const analyzeButton = document.getElementById("analyze-btn");
const errorMessage = document.getElementById("error-message");

const successModal = document.getElementById("success-modal");
const checkQualityBtn = document.getElementById("check-quality-btn");
const skipQualityBtn = document.getElementById("skip-quality-btn");


let draggedFile = "";
let selectedFiles = [];



window.onload = function () {

    loadUploadedFiles();

};




async function loadUploadedFiles() {


    const user_id = localStorage.getItem("user_id");


    if (!user_id) {

        errorMessage.innerText = "User not found";
        return;

    }


    try {


        let response = await fetch(
            `http://127.0.0.1:8000/uploadedfiles/${user_id}`
        );


        let data = await response.json();


        allFiles.innerHTML = "";


        if (!response.ok) {

            errorMessage.innerText = data.detail;
            return;

        }



        if (data.filenames.length === 0) {


            allFiles.innerHTML =
                "<p>No uploaded files found</p>";

            return;

        }



        data.filenames.forEach(filename => {


            let div = document.createElement("div");


            div.className = "file-card";


            div.draggable = true;



            div.innerHTML = `

                <div class="file-details">

                    <i class="fa-solid fa-file"></i>

                    <div>

                        <div class="file-name">
                            ${filename}
                        </div>

                    </div>

                </div>

            `;



            div.addEventListener(
                "dragstart",
                function () {

                    draggedFile = filename;

                }
            );



            allFiles.appendChild(div);


        });



    }


    catch(error) {


        errorMessage.innerText =
            "Unable to load uploaded files";


        console.log(error);


    }


}





dropArea.addEventListener(
    "dragover",
    function(e){

        e.preventDefault();

        dropArea.classList.add("dragover");

    }
);





dropArea.addEventListener(
    "dragleave",
    function(){

        dropArea.classList.remove("dragover");

    }
);





dropArea.addEventListener(
    "drop",
    function(e){


        e.preventDefault();


        dropArea.classList.remove("dragover");


        addSelectedFile(draggedFile);


    }
);






function addSelectedFile(filename){


    if(filename === ""){

        return;

    }



    if(selectedFiles.includes(filename)){

        return;

    }



    selectedFiles.push(filename);


    renderSelectedFiles();


}







function renderSelectedFiles(){


    selectedFilesContainer.innerHTML = "";



    if(selectedFiles.length === 0){


        selectedFilesContainer.innerHTML = `

            <div class="drop-message">

                <i class="fa-solid fa-cloud-arrow-down"></i>

                <p>Drag files here</p>

            </div>

        `;


        return;

    }



    selectedFiles.forEach(
        (filename,index)=>{


            let div = document.createElement("div");


            div.className="selected-file";



            div.innerHTML = `


                <div class="selected-name">

                    <i class="fa-solid fa-file"></i>

                    <span>${filename}</span>

                </div>



                <button 
                class="remove-btn"
                onclick="removeFile(${index})">


                    <i class="fa-solid fa-xmark"></i>


                </button>


            `;



            selectedFilesContainer.appendChild(div);


        }
    );

}






function removeFile(index){


    selectedFiles.splice(index,1);


    renderSelectedFiles();


}


window.removeFile = removeFile;







analyzeButton.addEventListener(
    "click",
    startAnalysis
);









async function startAnalysis(){



    if(selectedFiles.length === 0){


        errorMessage.innerText =
            "Please select at least one file";


        return;


    }




    const user_id =
        localStorage.getItem("user_id");



    if(!user_id){


        errorMessage.innerText =
            "User not found";


        return;


    }




    try{



        let response = await fetch(

            "http://127.0.0.1:8000/user/file/qualitycheck",

            {

                method:"POST",


                headers:{


                    "Content-Type":
                    "application/json"


                },



                body:JSON.stringify({


                    user_id:user_id,


                    filenames:selectedFiles


                })


            }

        );





        let data = await response.json();





        if(!response.ok){


            errorMessage.innerText =
                data.detail;


            return;


        }





        console.log(data);



        // Save quality id
        localStorage.setItem(
            "quality_id",
            data.quality_id
        );



        successModal.style.display="flex";



    }



    catch(error){



        console.log(error);



        errorMessage.innerText =
            "Server connection failed";


    }


}









checkQualityBtn.addEventListener(
"click",
function(){


    const quality_id =
        localStorage.getItem("quality_id");



    if(!quality_id){


        errorMessage.innerText =
            "Quality ID not found";


        return;


    }



    window.location.href =
    "qualityreport.html";


});








skipQualityBtn.addEventListener(
"click",
function(){


    successModal.style.display="none";


});







successModal.addEventListener(
"click",
function(e){


    if(e.target === successModal){

        successModal.style.display="none";

    }


});