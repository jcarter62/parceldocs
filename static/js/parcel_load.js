
function parcel_load() {
    let eid = 'parcel_list';
    let url = '/api/parcels';
    const Http = new XMLHttpRequest();
    Http.open('GET', url);
    Http.send();

    /*
    <div class="col-md-2" id="parel_list">
        Parcel list goes here.
    </div>
    <div class="col-md-10" id="parcel_data">
        Data Goes Here
    </div>
    */

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

window.addEventListener('load', parcel_load);
//document.onload = parcel_load();

window.addEventListener('load', (event) => {
  console.log('page loaded from parcel_load.js');
});