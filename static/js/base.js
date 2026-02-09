
const menu = document.getElementById('hamburgerMenu');
const left_sidebar = document.getElementById('leftSidebar');
const overlay = document.getElementById('sidebarOverlay');
const search_icon=document.getElementById('searchIcon');
const search_form=document.getElementById('searchForm');
// const cancel_btn=document.getElementById('cancelBtn');
const sidebar_links = document.querySelectorAll('.sidebar-link');
const current_page=window.location.pathname;
const posts_share=document.querySelectorAll('.copy-link');

sidebar_links.forEach(link=>{
    const path=new URL(link.href).pathname;
    link.classList.remove('active');
    if(path==current_page)link.classList.add('active');
});

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
    search_form.classList.toggle('active');
});


// cancel_btn.addEventListener('click',()=>{
//     search_form.classList.remove('active');
//     search_icon.style.display='block';
// })

posts_share.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        navigator.clipboard.writeText(this.dataset.url);
        alert('Link copied!');
    });
});