var checkboxInput = document.getElementById("newCategory");
checkboxInput.addEventListener('change', function() {
    var rad = document.filterForm.categoryRadio;
    if(!(rad.constructor === RadioNodeList)){
        rad = [rad];
    }
    for (var i = 0; i < rad.length; i++) {
        rad[i].checked = false;
    }
}
)

var rad = document.filterForm.categoryRadio;
if(!(rad.constructor === RadioNodeList)){
    rad = [rad];
}
for (var i = 0; i < rad.length; i++) {
        rad[i].addEventListener('change', function() {
            var checkboxInput = document.getElementById("newCategory");
            checkboxInput.checked = false;
        }
        )
}