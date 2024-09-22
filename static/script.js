$(document).ready(function() {
    const entity_unit_map = {
        width: ['centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'],
        depth: ['centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'],
        height: ['centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'],
        item_weight: ['gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'],
        maximum_weight_recommendation: ['gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'],
        voltage: ['kilovolt', 'millivolt', 'volt'],
        wattage: ['kilowatt', 'watt'],
        item_volume: ['centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart']
    };

    var $entitySelect = $('#entity-select');
    var $unitSelect = $('#unit-select');

    // Populate the entity dropdown
    for (var entity in entity_unit_map) {
        $entitySelect.append(`<option value="${entity}">${entity}</option>`);
    }

    // Handle changes in the entity dropdown
    $entitySelect.change(function() {
        var selectedEntity = $(this).val();

        // Clear the unit dropdown
        $unitSelect.empty();
        $unitSelect.append(`<option value="">-- Select a Unit --</option>`);

        // Populate the unit dropdown based on the selected entity
        if (selectedEntity) {
            var units = entity_unit_map[selectedEntity];
            units.forEach(function(unit) {
                $unitSelect.append(`<option value="${unit}">${unit}</option>`);
            });
        }
    });

    // Handle image drag and drop
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

        // Get selected entity and unit
        var selectedEntity = $('#entity-select').val();
        var selectedUnit = $('#unit-select').val();
        formData.append('entity', selectedEntity);
        formData.append('unit', selectedUnit);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                alert('Image uploaded successfully with entity: ' + selectedEntity + ' and unit: ' + selectedUnit);
            },
            error: function(error) {
                alert('Error uploading image: ' + error.responseText);
            }
        });
    }
});
