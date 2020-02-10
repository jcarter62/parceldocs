
function parcel_load() {
    let eid = 'parcel_list';
    let url = '/api/parcels';
    const Http = new XMLHttpRequest();
    Http.open('GET', url);
    Http.send();

    Http.onreadystatechange = function() {
        if ((this.readyState == 4) && (this.status == 200)) {
            let parcels = Http.responseText
            parcels = JSON.parse(parcels);
            let e = document.getElementById(eid);
            let r = '';
            for ( let i in parcels ) {
                r = r + parcels[i]['parcel_id'] + ':';
            }
            e.innerText = r;
            //e.innerHTML = html;
        }
    }
}

function parcel_lookup() {
    let timer = null;
    let delay = 1500;
    if (timer) {
        window.clearTimeout(timer);
    }
    timer = window.setTimeout(function () {
        timer = null;
        parcel_lookup_exec();
    }, delay);
}

function parcel_lookup_exec() {
    let item = document.getElementById('inp_parcel');
    if (item != null) {
        let value = item.value;
        if (value > '') {
            localStorage.setItem('inp_parcel', value);
        } else {
            localStorage.removeItem('inp_parcel');
        }
        console.log('inp_parcel = ' + value)
        parcel_partial_load(value);
    }
}

function save_selected_parcel(parcel_id) {
    localStorage.setItem('parcel_id', parcel_id);
}

function get_selected_parcel() {
    let value = localStorage.getItem('parcel_id');
    if ( value != null ) {
        return value;
    } else {
        return '';
    }
}

function parcel_load_value() {
    let value = localStorage.getItem('inp_parcel');
    if (value != null) {
        let element = document.getElementById('inp_parcel');
        element.value = value;
        parcel_partial_load(value);
    }
}

function parcel_partial_load(search_value) {
    let val = search_value;
    let url = '/api/parcel-search/' + val;
    const Http = new XMLHttpRequest();
    Http.open('GET', url);
    Http.send();

    Http.onreadystatechange = function () {
        if ((this.readyState == 4) && (this.status == 200)) {
            let parcels = Http.responseText;
            parcels = JSON.parse(parcels);
            let e = document.getElementById('parcel_list');
            let new_text = '';
            for (let i in parcels) {
                let tag = '<tr><td class="col-xs-4" ><a href="/selected/' + parcels[i]['parcel'] + '">'
                new_text = new_text + tag;
                new_text = new_text + parcels[i]['parcel'];
                new_text = new_text + '</a></td>';
                new_text = new_text + '<td class="col-xs-3">' + parcels[i]['files'] + '</td>';
                new_text = new_text + '<td class="col-xs-3">' + parcels[i]['size'] + '</td>';
                new_text = new_text + '</tr>';
            }
            new_text = new_text + '';
            e.innerHTML = new_text;
        }
    }
}

function parcel_selected(parcel_id) {
    console.log(parcel_id);
    save_selected_parcel(parcel_id);
    retrieve_parcel_files(parcel_id);
    let elem = document.getElementById('fileElemParcel');
    elem.value = parcel_id;
}

function retrieve_parcel_files(parcel_id) {
    let url = '/api/parcel-files/' + parcel_id;
    const Http = new XMLHttpRequest();
    Http.open('GET', url);
    Http.send();

    Http.onreadystatechange = function () {
        if ((this.readyState == 4) && (this.status == 200)) {
            let file_list = Http.responseText;
            let files = JSON.parse(file_list);
            let new_text = '';
            if (files.length <= 0) {
                new_text = '<h3>No Files for parcel ' + parcel_id + '</h3>';
            } else {
                new_text = '';
                for (let i in files) {
                    let encoded = window.btoa(files[i].fullpath);
                    let tag = '<div class="row"><a target="_blank" href="/sendfile/' + encoded + '">';
                    new_text = new_text + tag;
                    new_text = new_text + files[i].name;
                    new_text = new_text + '</a></div>';
                }
                new_text = new_text + '';
            }
            let e = document.getElementById('parcel_files');
            e.innerHTML = new_text;
        }
    }
}

function rename_file(fileinfo) {
    console.log(fileinfo)
}

// let parcel_id = ''
// let win = null;

function dragdrop_init() {
    // Ref: https://youtu.be/hqSlVvKvvjQ
    let drop_zone = document.getElementById('dropzone');
    let visible_parcel_id = document.getElementById('parcel_id').innerText;

    drop_zone.ondragover = function() {
        this.className = 'dropzone dragover';
        return false;
    }

    drop_zone.ondragleave = function() {
        this.className = 'dropzone';
        return false;
    }

    function upload(files){
        let formData = new FormData();
        let xhr = new XMLHttpRequest();
        let i = 0;

        for (i=0; i<files.length; i++) {
            let name = 'file' + i.toString();
            formData.append(name, files[i]);
        }
        formData.append('parcel_id', visible_parcel_id);

        xhr.addEventListener('load', function(e) {
            let info = e.target;
            if (( info.readyState == 4 ) && (info.status == 200)) {
                location.reload();
            }
        });

        xhr.open('post', '/uploadfiles');
        xhr.send(formData);
    }

    drop_zone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'dropzone';
        upload(e.dataTransfer.files);
    }
}

function parcel_files_init(parcel_id) {
    function get_details(){
        let xhr = new XMLHttpRequest();

        xhr.addEventListener('load', function(e) {
            let info = e.target;
            if (( info.readyState == 4 ) && (info.status == 200)) {
                console.log(info);
            }
        });

        let url = '/api/parcel-doc-info/' + parcel_id;
        xhr.open('get', url);
    }

    get_details();
}

