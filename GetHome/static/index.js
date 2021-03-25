

function createHtmlElement_HouseDataList() {
    function addHouseFormElement(data)
    {
        let ele =
        `
            <div>
                <form action="/house">
                    <li><span>價錢</span> <input type="text" name="price" value=${data["price"]}></li>
                    <li><span>格局</span> <input type="text" name="house_pattern" value=${data["house_pattern"]}></li>
                    <li><span>屋齡</span> <input type="text" name="age" value=${data["age"]}></li>
                    <li><span>樓層</span> <input type="text" name="floors" value=${data["floors"]}></li>
                    <li><span>型態</span> <input type="text" name="building_type" value=${data["building_type"]}></li>
                    <li><span>地址</span> <input type="text" name="address" value=${data["address"]}></li>
                    <li><span>座向</span> <input type="text" name="direction" value=${data["direction"]}></li>
                    <li><span>社區</span> <input type="text" name="apartment_complex" value=${data["apartment_complex"]}></li>
                    <li><span>權狀坪數</span> <input type="text" name="ownership_size" value=${data["ownership_size"]}></li>
                    <li><span>土地坪數</span> <input type="text" name="land_size" value=${data["land_size"]}></li>
                    <li><span>主建物坪數</span> <input type="text" name="main_building_size" value=${data["main_building_size"]}></li>
                    <li><span>資料來源</span> <input type="text" name="source" value=${data["source"]} maxlength="1000" size="50"></li>
                    <li name="id" hidden>${data["id"]}</li>
                </form>
                <button class=delete_house>Delete</button>
                <button class=update_house>Update</button>
            </div>
            <hr>
        `;
        $("#house_list").prepend(ele)
    }

    function bindBtnEvent() {
        // bind delete btn
        $(".delete_house").click(function(){
            let id = $(this).parent().find('li[name ="id"]').text();

            let xhr = new XMLHttpRequest();
            xhr.open("DELETE", "/house?id="+id);
            xhr.onloadend = (function(e){
                location.reload();
            });
            xhr.send();
        });

        // bind update btn
        $(".update_house").click(function(){
            let form = $(this).parent().children("form")[0];
            let id = $(this).parent().find('li[name ="id"]').text();

            $.ajax({
                type: 'put',
                url: "/house?id=" + id,
                processData: false, // not convert to query string
                contentType: false, // use false instead of multipart/form-data to keep boundary info
                data: new FormData(form),
                success: function(){
                    location.reload();
                }
            });
        });
    }

    // get list from server
    $.ajax({
        url: "/house",
        type: "GET",
        dataType: "json",
        success: function(jData) {
            // get house data list
            $.each(jData, function(index, element){
                addHouseFormElement(element)
            });

            bindBtnEvent();
        }
    });
}

function createDynamicHtmlElements() {
    createHtmlElement_HouseDataList();
}

function bindHtmlElementEvent() {
    // change default submit behavior
    $('#add_house_data_form').submit(function(e) {
        let form_html_elem = $(this)[0];
        let actionurl = e.currentTarget.action;

        //prevent Default functionality
        e.preventDefault();

        $.ajax({
            type: 'post',
            url: actionurl,
            processData: false, // not convert to query string
            contentType: false, // use false instead of multipart/form-data to keep boundary info
            data: new FormData( form_html_elem ),
            success: function(){
                location.reload();
            }
        });
    });
}


// run
bindHtmlElementEvent();
createDynamicHtmlElements();
