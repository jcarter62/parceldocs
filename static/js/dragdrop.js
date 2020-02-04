
class DragDrop {

    constructor(){
        this.bHaveFileAPI = (window.File) && (window.FileReader);
        if ( ! this.bHaveFileAPI ) {
            alert('This browser does not support the File API');
            return;
        }

        document.getElementById('parcel_files').addEventListener('change', this.onFileChanged);
    }

    onFileChanged(evt){
        alert("You selected a file: " + evt.target.files[0].name);
    }
}

//let dd = DragDrop();

window.addEventListener('load', (event) => {
  let dragdrop = new DragDrop();
});