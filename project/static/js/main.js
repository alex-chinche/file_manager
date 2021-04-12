jQuery(document).ready(function ($) {
    $('a.delete').click(function () {
        var confirmation = confirm("Are you sure you want to delete this file?");
        if (confirmation == true) {
            self.location = "/delete/" + this.dataset.id;
        }
    });
});


function addFile() {
    $('#uploadFile').submit()
};

