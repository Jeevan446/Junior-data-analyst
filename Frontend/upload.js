const dropArea=document.getElementById("drop-area");

const fileInput=document.getElementById("fileInput");

const fileList=document.getElementById("file-list");

const uploadedFiles=document.getElementById("uploaded-files");

const errorMessage=document.getElementById("error-message");

const analyzeButton=document.getElementById("analyze-btn");


let files=[];



window.onload=function(){

loadUploadedFiles();

};




fileInput.addEventListener("change",()=>{

addFiles(Array.from(fileInput.files));

fileInput.value="";

});





dropArea.addEventListener("dragover",(e)=>{

e.preventDefault();

dropArea.style.background="#f8fafc";

});




dropArea.addEventListener("dragleave",()=>{

dropArea.style.background="white";

});




dropArea.addEventListener("drop",(e)=>{

e.preventDefault();

dropArea.style.background="white";

addFiles(Array.from(e.dataTransfer.files));

});





function addFiles(newFiles){


newFiles.forEach(file=>{


let ext=file.name.split(".").pop().toLowerCase();


if(
ext==="csv" ||
ext==="xlsx" ||
ext==="xls"
){


let exists=files.some(
f=>f.name===file.name
);


if(!exists){

files.push(file);

}


}
else{

errorMessage.innerText="Only CSV and Excel files are allowed";

}


});


showFiles();

}





function showFiles(){


fileList.innerHTML="";


files.forEach((file,index)=>{


let div=document.createElement("div");


div.className="file-item";


div.innerHTML=`

<div class="file-name">

<i class="fa-solid fa-file"></i>

${file.name}

</div>


<button class="remove-file" onclick="removeFile(${index})">

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







async function loadUploadedFiles(){


let user_id=localStorage.getItem("user_id");


if(!user_id)
return;



try{


let response=await fetch(

`http://127.0.0.1:8000/uploadedfiles/${user_id}`

);



let data=await response.json();



uploadedFiles.innerHTML="";



if(data.filenames){


data.filenames.forEach(filename=>{


let div=document.createElement("div");


div.className="uploaded-file";


div.innerHTML=`

<i class="fa-solid fa-file"></i>

<span>${filename}</span>

`;


uploadedFiles.appendChild(div);



});


}


}

catch(error){

console.log(error);

}


}







analyzeButton.addEventListener("click",uploadFiles);







async function uploadFiles(){



if(files.length===0){

errorMessage.innerText="Please select at least one file";

return;

}



let user_id=localStorage.getItem("user_id");



if(!user_id){

errorMessage.innerText="User not found";

return;

}



let formData=new FormData();



files.forEach(file=>{

formData.append("files",file);

});



formData.append("user_id",user_id);




try{


let response=await fetch(

"http://127.0.0.1:8000/uploadfiles",

{

method:"POST",

body:formData

}

);




let data=await response.json();



if(!response.ok){

errorMessage.innerText=data.detail;

return;

}



await loadUploadedFiles();



files=[];

showFiles();



errorMessage.innerText="";



}

catch(error){


errorMessage.innerText="Server connection failed";


}



}