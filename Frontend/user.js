const description = document.getElementById("description");
const wordCount = document.getElementById("word-count");
const errorMessage = document.getElementById("error-message");



description.addEventListener("input", function(){

    let words = description.value
    .trim()
    .split(/\s+/)
    .filter(word => word.length > 0);



    if(description.value.trim()===""){

        words=[];

    }


    wordCount.innerText = `Words: ${words.length} / 100`;


    if(words.length > 100){

        errorMessage.innerText =
        "Description cannot contain more than 100 words";

    }
    else{

        errorMessage.innerText="";

    }


});




function startAnalysis(){


    let name =
    document.getElementById("name").value;


    let company =
    document.getElementById("company").value;


    let descriptionText =
    description.value.trim();



    let words = descriptionText
    .split(/\s+/)
    .filter(word => word.length > 0);



    if(descriptionText !== "" && words.length > 100){

        errorMessage.innerText =
        "Please reduce description below 100 words";

        return;

    }



    let userData={

        name:name,

        company:company,

        description:descriptionText

    };



    localStorage.setItem(
        "userInfo",
        JSON.stringify(userData)
    );



    window.location.href="analysis.html";


}





function skipInfo(){


    localStorage.removeItem("userInfo");


    window.location.href="analysis.html";


}