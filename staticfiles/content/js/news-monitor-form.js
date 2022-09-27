function setActiveCategory(catValue) {
    
    console.log('sectActiveCategory received value:' + catValue)    
    if($('#id_categories option[value=' + catValue + ']').attr('selected')=='selected') {
        $('#id_categories option[value=' + catValue + ']').removeAttr("selected");
        $('#categories-'+catValue).removeClass("btn-primary");
        $('#categories-'+catValue).addClass("btn-light");
    } else {
        $('#id_categories option[value=' + catValue + ']').attr('selected', 'selected');
        $('#categories-'+catValue).removeClass("btn-light");
        $('#categories-'+catValue).addClass("btn-primary");
    }
    
}

function submitNewsMonitorForm() {
        $("#newsMonitorForm").submit();     
}


function setActiveExpertLevel(exValue) { 
    
    $('#id_expert_level option[value=' + exValue + ']').attr('selected', 'selected');
    $('#expert_level-PRO').removeClass("btn-primary");
    $('#expert_level-PRO').addClass("btn-light");
    $('#expert_level-INTERMEDIATE').removeClass("btn-primary");
    $('#expert_level-INTERMEDIATE').addClass("btn-light");
    $('#expert_level-BASIC').removeClass("btn-primary");
    $('#expert_level-BASIC').addClass("btn-light");

    $('#expert_level-'+exValue).removeClass("btn-light");
    $('#expert_level-'+exValue).addClass("btn-primary");

}

function setActiveTags(tagValue) {
    $('#id_tags option[value=' + tagValue + ']').attr('selected', 'selected');
}

function removeActiveTag(tagValue) {
    $('#id_tags option[value=' + tagValue + ']').removeAttr('selected')
}

function appendSymbols(symbols) {
    $.each(symbols, function(i, item) {
        $('#id_projects option[value=' + symbols[i].project + ']').html($('#id_projects option[value=' + symbols[i].project + ']').html() + ' (' + symbols[i].symbol + ')')
    });
}   


function setActiveSentiment() {
    const sentiment = $("#id_sentiment").val();
    if (sentiment=='POSITIVE') {
        $('#sentiment-positive').html('<span class="iconify" data-icon="fluent:checkmark-12-filled" style="color: white;" data-width="50"></span>');
    }
    if (sentiment=='NEUTRAL') {
        $('#sentiment-neutral').html('<span class="iconify" data-icon="fluent:checkmark-12-filled" style="color: white;" data-width="50"></span>');
    }
    if (sentiment=='NEGATIVE') {
        $('#sentiment-negative').html('<span class="iconify" data-icon="fluent:checkmark-12-filled" style="color: white;" data-width="50"></span>');
    }    
}

$(document).ready(function() {    

    setActiveSentiment()

    $('#id_projects').select2({theme: "bootstrap-5", selectionCssClass: "select2--small", dropdownCssClass: "select2--small"});
    
    
    var tagDatabase=[];
    $.getJSON('/api/tags')
    .done(function(response) {
        console.log(response)
        $.each(response.tag_list, function(i, subject){
            tagDatabase.push(subject.name);
        })
        console.log("tagDataBase: " + tagDatabase);
    })
    .fail(function(err){
        console.log("$.getJSON('/api/tags') failed")
    })

    $('#id_tags').select2({
        tags: true,
        theme: "bootstrap-5", 
        selectionCssClass: "select2--small", 
        dropdownCssClass: "select2--small",
        createTag: function (params) {
            var term = $.trim(params.term);
            
            if (term === '') {
              return null;
            }
        
            return {
              id: term,
              text: term,
              isNew: true // add additional parameters
            }
          }
    }).on("select2:select", function(e) {

        if(tagDatabase.indexOf(e.params.data.text) !== -1) {
            console.log(e.params.data.text + " already in database")
        } else {
            addTag(e.params.data.text)
            window.location.reload()
            console.log("adding " + e.params.data.text + " to database")
        }

        setActiveTags(e.params.data.id);

    }).on('select2:unselecting', function (e) {

        console.log(e.params.args.data.id)
        removeActiveTag(e.params.args.data.id)
    
    });

    $('#sentiment-positive').click(function(e){
        
        $('#sentiment-positive').html('<span class="iconify" data-icon="fluent:checkmark-12-filled" style="color: white;" data-width="50"></span>');
        $('#sentiment-neutral').html('');
        $('#sentiment-negative').html('');
        $('#id_sentiment').prop('value', 'POSITIVE');
    });

    $('#sentiment-neutral').click(function(e){
        
        $('#sentiment-positive').html('');
        $('#sentiment-neutral').html('<span class="iconify" data-icon="fluent:checkmark-12-filled" style="color: white;" data-width="50"></span>');
        $('#sentiment-negative').html('');
        $('#id_sentiment').prop('value', 'NEUTRAL');
    });

    $('#sentiment-negative').click(function(e){
        
        $('#sentiment-positive').html('');
        $('#sentiment-neutral').html('');
        $('#sentiment-negative').html('<span class="iconify" data-icon="fluent:checkmark-12-filled" style="color: white;" data-width="50"></span>');
        $('#id_sentiment').prop('value', 'NEGATIVE');
    });

    /* Generate Categories buttons based on select input */

    $('#id_categories option').each(function(index){
        $('#categories').append('<button class="btn btn-light generated-btn" id="categories-' + $(this).prop('value') + '" onclick="setActiveCategory(' + $(this).prop('value') + ')">' + $(this).prop('text') + '</button>');
    });

    /* Activate buttons of selected items */

    var values = $('#id_categories').val();
    for(let value of values) {
        $('#categories-'+value).removeClass("btn-light");
        $('#categories-'+value).addClass("btn-primary");
    }

    /* Generate Expert Level Buttons */

    $('#id_expert_level option').each(function(index){
        $('#expert_level').append('<button class="btn btn-light generated-btn" id="expert_level-' + $(this).prop('value') + '"onclick="setActiveExpertLevel(\'' + $(this).prop('value') + '\')">' + $(this).prop('text') + '</button>');
    });    

    /* Activate buttons of selected Expert Levels */

    var value = $('#id_expert_level').val();
    $('#expert_level-'+value).removeClass("btn-light");
    $('#expert_level-'+value).addClass("btn-primary");
    

    $('button').click(function(event) {
        event.preventDefault();
    });

    setActiveExpertLevel("BASIC")

});