const dropArea = document.getElementById("drop-area");

const fileInput = document.getElementById("fileInput");

const fileList = document.getElementById("file-list");

const errorMessage = document.getElementById("error-message");

const analyzeButton = document.getElementById("analyze-btn");


let files = [];




// file select

fileInput.addEventListener("change", function(){


    addFiles(Array.from(fileInput.files));


    fileInput.value="";


});





// drag over

dropArea.addEventListener("dragover", function(e){


    e.preventDefault();


    dropArea.style.background="#f8fafc";


});





// drag leave

dropArea.addEventListener("dragleave", function(){


    dropArea.style.background="white";


});






// drop

dropArea.addEventListener("drop", function(e){


    e.preventDefault();


    dropArea.style.background="white";


    addFiles(
        Array.from(e.dataTransfer.files)
    );


});







function addFiles(newFiles){



    newFiles.forEach(file=>{


        let extension =
        file.name
        .split(".")
        .pop()
        .toLowerCase();




        if(
            extension==="csv" ||
            extension==="xlsx" ||
            extension==="xls"
        ){


            // avoid duplicate files in frontend

            let alreadyExist =
            files.some(
                existingFile =>
                existingFile.name === file.name
            );



            if(!alreadyExist){

                files.push(file);

            }


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



    files.forEach((file,index)=>{



        let div =
        document.createElement("div");



        div.className="file-item";




        div.innerHTML =

        `

        <div class="file-name">

        <i class="fa-solid fa-file"></i>

        ${file.name}

        </div>



        <button 
        class="remove-file"
        onclick="removeFile(${index})">


        <i class="fa-solid fa-xmark"></i>


        </button>


        `;



        fileList.appendChild(div);



    });



}







function removeFile(index){


    files.splice(index,1);


    showFiles();


}








analyzeButton.addEventListener(
    "click",
    startAnalysis
);








async function startAnalysis(){



    if(files.length===0){


        errorMessage.innerText =
        "Please select at least one file";


        return;


    }







    const user_id =
    localStorage.getItem("user_id");





    if(!user_id){


        errorMessage.innerText =
        "User not found. Please create account again";


        return;


    }








    let formData =
    new FormData();







    files.forEach(file=>{


        formData.append(
            "files",
            file
        );


    });







    formData.append(
        "user_id",
        user_id
    );








    try{



        let response =
        await fetch(

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