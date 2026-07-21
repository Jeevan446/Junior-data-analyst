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



async function createUser(company, descriptionText){

    let userData = {
        company_type: company,
        company_description: descriptionText
    };


    try{

        let response = await fetch(
            "http://127.0.0.1:8000/createuser",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify(userData)
            }
        );


        let data = await response.json();


        if(!response.ok){

            errorMessage.innerText = data.detail;
            return false;

        }


        localStorage.setItem(
            "user_id",
            data.user.user_id
        );


        return true;


    }
    catch(error){

        console.log(error);

        errorMessage.innerText =
        "Unable to connect with server";

        return false;
    }

}




async function startAnalysis(){

    let company =
    document.getElementById("company")
    .value
    .trim();


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


    let success = await createUser(
        company,
        descriptionText
    );


    if(success){

        window.location.href="upload.html";
    }

}




async function skipInfo(){

    let success = await createUser(
        "",
        ""
    );


    if(success){

        window.location.href="upload.html";
    }

}