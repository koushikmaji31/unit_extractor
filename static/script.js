$(document).ready(function() {
    $('#drop-area').on('dragover', function(e) {
        e.preventDefault();
        $(this).addClass('dragover');
    });

    $('#drop-area').on('dragleave', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
    });

    $('#drop-area').on('drop', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');

        var files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    });

    $('#drop-area').click(function() {
        $('#image-input').click();
    });

    $('#image-input').change(function() {
        var files = this.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    });

    function uploadFile(file) {
        var formData = new FormData();
        formData.append('image', file);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                alert('Image uploaded successfully!');
            },
            error: function(error) {
                alert('Error uploading image: ' + error.responseText);
            }
        });
    }
});
$(document).ready(function() {
    $('#drop-area').on('dragover', function(e) {
        e.preventDefault();
        $(this).addClass('dragover');
    });

    $('#drop-area').on('dragleave', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
    });

    $('#drop-area').on('drop', function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');

        var files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    });

    $('#drop-area').click(function() {
        $('#image-input').click();
    });

    $('#image-input').change(function() {
        var files = this.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    });

    function uploadFile(file) {
        var formData = new FormData();
        formData.append('image', file);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                alert('Image uploaded successfully!');
            },
            error: function(error) {
                alert('Error uploading image: ' + error.responseText);
            }
        });
    }
});
