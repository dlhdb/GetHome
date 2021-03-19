


// bind click event to all delete btn
$(".delete_house").click(function(){
    let id = $(this).parent().children('li[name ="id"]').text();
    let url = window.location.origin+"/house"
    
    let formData = new FormData();
    formData.append("id", id);
    let xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/house");
    xhr.onloadend = (function(e){
        location.reload();
    });
    xhr.send(formData);
});

// change default submit behavior
$('#add_house_data_form').submit(function(e) {
    let form = $(this)[0];
    let actionurl = e.currentTarget.action;

    //prevent Default functionality
    e.preventDefault();

    $.ajax({
        type: 'post',
        url: actionurl,
        processData: false, // not convert to query string
        contentType: false, // use false instead of multipart/form-data to keep boundary info
        data: new FormData( form ),
        success: function(){
            location.reload();
        }
    });
});