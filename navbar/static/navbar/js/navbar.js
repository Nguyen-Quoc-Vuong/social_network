/* user-settings */
var userSettings = document.querySelector(".user-settings");
var LoadMoreBackground =document.querySelector(".btn-LoadMore");
var listNotif = document.querySelector(".list_notif");
        function UserSettingToggle(){
            userSettings.classList.toggle("user-setting-showup-toggle");
        }
        function ListNotifToggle() {
            listNotif.classList.toggle("list-notif-showup-toggle");
        }
        // function LoadMoreToggle(){
        //     LoadMoreBackground.classList.toggle("loadMoreToggle");
        // };

/* change-color */
const currentUrl = window.location.pathname;
// console.log(currentUrl);

if (currentUrl.includes("/")) {
    document.getElementById("home").classList.add("active");
} else if (currentUrl.includes("/friend")) {
    document.getElementById("friend").classList.add("active");
} else if (currentUrl.includes("/userprofiles")) {
    document.getElementById("home").classList.remove("active");
    document.getElementById("friend").classList.remove("active");
}

//Sử lý phần search
const searchInput = document.getElementById('search-input');
const nav_bar = document.querySelector("ul");
function remove_search_list(event){
    console.log("danh sach:",event.target.parentNode.parentNode.parentNode.className);
    console.log("danh sach con:",event.target.parentNode.parentNode.className);
    if(event.target.parentNode.parentNode.parentNode.className === "search-list"){
        event.target.parentNode.parentNode.parentNode.remove();
    }else if(event.target.parentNode.parentNode.className === "search-list"){
        event.target.parentNode.parentNode.remove();
    }
    searchInput.value = null;
}

searchInput.addEventListener('keyup', function(event) {
  // Kiểm tra nếu phím nhấn là Enter (mã ASCII: 13)
  if (event.keyCode === 13 && searchInput.value !== null && searchInput.value !== "") {
    console.log(searchInput.value);
    var formdata = new FormData();
    formdata.append("name",searchInput.value);
    var url_search = "/navbar/searchlist/";
    fetch(url_search,{
        method:"POST",
        body:formdata,
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data);
        var a = 
        `
        <div style="display: flex;flex-direction: row;align-items: center;">
            <div style="font-size: large; color: rgb(0, 110, 255); margin: 10px;text-decoration: underline;display: block;margin-right: 70px;"> Danh sách tìm kiếm </div>
            <button type="button" class="remove-search-list" onclick="remove_search_list(event)">
                <i class="fas fa-times" aria-hidden="true"></i>
            </button>
        </div>`;
        data.forEach(function(people){
            console.log(people.search_user.first_name)
            var url = `/userprofiles/?id=${people.search_user.id}`;
            a+=`
            <a href="${url}" style="text-decoration: none;color:black;" id="${people.search_user.id}">
            <div class="person_being_searched">
                <div class="person_being_searched_img">
                    <img style=" display: flex ; width: 100%;height: 100%;" src="${people.search_user.avatar}" alt="Card Image">
                </div>
                <div>
                    <h3>${people.search_user.name}</h3>
                </div>
            </div>
            </a>`;
        })
        var newDiv = document.createElement("div");
        newDiv.classList.add("search-list");
        newDiv.innerHTML = a;
        nav_bar.appendChild(newDiv);
    })
  }
});

