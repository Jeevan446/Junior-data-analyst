const dropArea = document.getElementById("drop-area");

const fileInput = document.getElementById("fileInput");

const fileList = document.getElementById("file-list");

const errorMessage = document.getElementById("error-message");

const analyzeButton = document.getElementById("analyze-btn");


let files = [];



// Select files

fileInput.addEventListener("change", function(){


    addFiles(Array.from(fileInput.files));


    fileInput.value="";


});




// Drag over

dropArea.addEventListener("dragover", function(e){

    e.preventDefault();

    dropArea.style.background="#f8fafc";

});




// Drag leave

dropArea.addEventListener("dragleave", function(){


    dropArea.style.background="white";


});




// Drop files

dropArea.addEventListener("drop", function(e){


    e.preventDefault();


    addFiles(Array.from(e.dataTransfer.files));


});





function addFiles(newFiles){


    newFiles.forEach(file=>{


        let extension = file.name
        .split(".")
        .pop()
        .toLowerCase();



        if(
            extension==="csv" ||
            extension==="xlsx" ||
            extension==="xls"
        ){

            files.push(file);

        }
        else{

            errorMessage.innerText =
            "Only CSV and Excel files are allowed";

        }


    });


    showFiles();

}






function showFiles(){


    fileList.innerHTML="";


    files.forEach(file=>{


        let div=document.createElement("div");


        div.className="file-item";


        div.innerHTML =
        `
        <i class="fa-solid fa-file"></i>
        ${file.name}
        `;


        fileList.appendChild(div);


    });


}






analyzeButton.addEventListener(
    "click",
    startAnalysis
);







async function startAnalysis(){



    // Check files

    if(files.length===0){


        errorMessage.innerText =
        "Please select at least one file";


        return;

    }




    // Get user id

    const user_id =
    localStorage.getItem("user_id");




    if(!user_id){


        errorMessage.innerText =
        "User not found. Please create account again";


        return;

    }





    let formData = new FormData();





    // Add files

    files.forEach(file=>{


        formData.append(
            "files",
            file
        );


    });






    // Add user id

    formData.append(
        "user_id",
        user_id
    );







    try{


        let response = await fetch(

            "http://127.0.0.1:8000/uploadfiles",

            {

                method:"POST",

                body:formData

            }

        );






        let data =
        await response.json();






        if(!response.ok){


            errorMessage.innerText =
            data.detail;


            return;


        }





        console.log(data);





        window.location.href =
        "dashboard.html";



    }



    catch(error){


        console.log(error);


        errorMessage.innerText =
        "Server connection failed";


    }



}