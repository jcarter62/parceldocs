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
            let new_text = '<dl>';
            for (let i in parcels) {
                let tag = '<div class="row" onclick="parcel_selected(\'' + parcels[i] + '\');">';
                new_text = new_text + tag;
                new_text = new_text + parcels[i];
                new_text = new_text + '</div>';
            }
            new_text = new_text + '</dl>';
            e.innerHTML = new_text;
        }
    }
}

function parcel_selected(parcel_id) {
    console.log(parcel_id);
    retrieve_parcel_files(parcel_id);

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
                new_text = '<dl>';
                for (let i in files) {
                    let encoded = window.btoa(files[i].fullpath);
                    let tag = '<div class="row"><a target="_blank" href="/sendfile/' + encoded + '">';
                    new_text = new_text + tag;
                    new_text = new_text + files[i].name;
                    new_text = new_text + '</a></div>';
                }
                new_text = new_text + '</dl>';
            }
            let e = document.getElementById('parcel_files');
            e.innerHTML = new_text;
        }
    }
}

window.addEventListener('load', parcel_load_value);

// parcel_load_value();

window.addEventListener('load', (event) => {
  console.log('page loaded from parcel_input.js');
});