if(localStorage['theme']=='dark'){
    document.body.classList.add('dark');
    try{
        document.querySelector('#img-logo').src = '/static/logo/photo_2022-09-06_21-20-111.jpg';
    } catch (e){};
    document.querySelectorAll('.course-img').forEach(el=>{
        el.src = '/static/logo/courses.png';
    });
} else{
    document.body.classList.remove('dark');
    try{
        document.querySelector('#img-logo').src = '/static/logo/photo_2022-09-06_21-20-11.jpg';
    } catch (e){};
    document.querySelectorAll('.course-img').forEach(el=>{
        el.src = '/static/logo/light-course.png';
    });
};
var menu = document.querySelector('#sidebar-toogle')
if(menu){
    menu.addEventListener('click', ()=>{
        document.querySelector('.sidebar').classList.toggle('open');
    });
};
document.addEventListener('mouseup', (e) => {
    if (!e.target.classList.contains('sidebar') && !e.target.classList.contains('sidebar_toggler') && !e.target.classList.contains('dropdown-center') && !e.target.classList.contains('sidebar-dr-opener')) {
        document.querySelector('.sidebar').classList.remove('open');
    }
});

    $.ajax(
        {
            type: 'GET',
            url: `/notification/`,
            success: (data) => {
                try{
                    var notifications = document.querySelector('#notifications');
                    var html = '';
                    if(Object.values(data['unread_messages']).length!==0){
                    for(let [key, value] of Object.entries(data)){
                        for(let [key1, value1] of Object.entries(value)){
                            html += `
                                <li><a class="dropdown-item text-white" href="${value1.url}">${key1} - ${value1.messages}</a></li>
                            `;
                        };
                    };}else{
                        html = '<li><a class="dropdown-item text-white" href="#">Sizda hech qanday bildirishnoma yo\'q</a></li>';
                    };
                    notifications.innerHTML = html;
                } catch (e){
                }
            },
            error: e=>console.error(e)
        }
    );
document.querySelectorAll('table').forEach(el => {
    el.classList.add('table-hover', 'table-striped', 'table-borderless');
},
);
document.querySelectorAll('th').forEach(el => {
    el.classList.add('p-2');
},
);
document.querySelectorAll('td').forEach(el => {
    el.classList.add('p-2');
},
);
var theme = document.querySelector('#theme-toggler');
theme.addEventListener('click', ()=>{
    if(localStorage['theme']==='dark'){
        document.body.classList.remove('dark');
        theme.classList.remove('fa-sun');
        theme.classList.add('fa-moon');
        localStorage.setItem('theme', 'light');
        try{
            document.querySelector('#img-logo').src = '/static/logo/photo_2022-09-06_21-20-11.jpg';
        } catch (e){};
        
        document.querySelectorAll('.course-img').forEach(el=>{
            el.src = '/static/logo/light-course.png';
        });
    } else{
        document.body.classList.add('dark');
        theme.classList.add('fa-sun');
        theme.classList.remove('fa-moon');
        localStorage.setItem('theme', 'dark');
        try{
            document.querySelector('#img-logo').src = '/static/logo/photo_2022-09-06_21-20-111.jpg';
        } catch (e){};
        document.querySelectorAll('.course-img').forEach(el=>{
            el.src = '/static/logo/courses.png';
        });
    };
});
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

var progress_item = document.querySelector('#progress-item')
if (progress_item){
    progress_item.style.width = progress_item.innerHTML;
}