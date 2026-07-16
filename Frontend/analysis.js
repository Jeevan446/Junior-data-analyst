const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("file-list");

let files = [];



fileInput.addEventListener("change", function(){

    addFiles(Array.from(fileInput.files));

    fileInput.value = "";

});



dropArea.addEventListener("dragover", function(e){

    e.preventDefault();

    dropArea.style.background="#f8fafc";

});



dropArea.addEventListener("dragleave", function(){

    dropArea.style.background="white";

});



dropArea.addEventListener("drop", function(e){

    e.preventDefault();

    addFiles(Array.from(e.dataTransfer.files));

});



function addFiles(newFiles){


    newFiles.forEach(file=>{


        let extension = file.name.split(".").pop().toLowerCase();


        if(
            extension === "csv" ||
            extension === "xlsx" ||
            extension === "xls"
        ){

            files.push(file);

        }
        else{

            alert("Please select only CSV and Excel files");

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
        `<i class="fa-solid fa-file"></i> ${file.name}`;


        fileList.appendChild(div);


    });


}