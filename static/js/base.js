
const menu = document.getElementById('hamburgerMenu');
const left_sidebar = document.getElementById('leftSidebar');
const overlay = document.getElementById('sidebarOverlay');
const search_icon=document.getElementById('searchIcon');
const search_form=document.getElementById('searchForm');
const cancel_btn=document.getElementById('cancelBtn');
const sidebar_links = document.querySelectorAll('.sidebar-link');


function toggle_class() {
    menu.classList.toggle('active');
    left_sidebar.classList.toggle('show');
    overlay.classList.toggle('show');
}
menu.addEventListener('click', toggle_class);
overlay.addEventListener('click', toggle_class);

sidebar_links.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 980) {
            toggle_class();
        }
    });
});

search_icon.addEventListener('click',()=>{
    search_form.classList.add('active');
    search_icon.style.display='none';
});

cancel_btn.addEventListener('click',()=>{
    search_form.classList.remove('active');
    search_icon.style.display='block';
})