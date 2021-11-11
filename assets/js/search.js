jQuery(function ($) {
    add_taxonomy_tree()
    $("#treeview").shieldTreeView();
});

const sendData = () => {
    let fD = new FormData();
    let files = document.getElementById("filepicker").files
    console.log(files)
    fD.append('image', files[0])
    fD.append('insect', $('#Insect').val())
    fD.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value)
    $.ajax({
        url: '/classification-insect/',
        type: 'POST',
        data: fD,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            data = JSON.parse(data)
            console.log(data)
            let htm = ''
            for (let i = 0; i < data.length; i++) {

                htm += `
                    <div class="left">
                        <img src="`+data[i].img+`" alt="">
                    </div>
                    <div class="right">
                        <a href="/detail/`+ data[i].slug +`">
                            <h3>`+ data[i].name +`</h3>
                        </a>
                        <h4>Score: `+ data[i].score +`</h4>
                        `+ data[i].characteristic +`
                    </div>
                `
            }

            console.log(htm)
            $("#search_result").html(htm)
        }
    });
}

const get_taxonomy_data = () => {
    let req = new XMLHttpRequest();
    req.open('GET','/get_taxonomy_tree', false)
    req.send(null)
    return JSON.parse(req.responseText);
}

let kingdom
let phylum
let classes
let order
let family
let genus
let insect

const findStringInArray = (string, arr) => {
    for (let i = 0; i < arr.length; i++) {
        for (let j in arr[i].fields) {
            if (j == string)
                return true
        }
    }
    return false
}

const add_taxonomy_tree = () => {
    //Kingdom, Phylum, Classes, Order, Family, Genus
    data = get_taxonomy_data()
    kingdom = data[0]
    phylum = data[1]
    classes = data[2]
    order = data[3]
    family = data[4]
    genus = data[5]
    insect = data[6]
    let obj = {}

    obj.name = kingdom[0].pk
    obj.phylum = []
    phylum.map(_phylum => {
        let tmp_classes = [];
        classes.map(_classes => {
            let tmp_order = [];
            order.map(_order => {
                let tmp_family = []

                family.map(_family => {
                    let tmp_genus = []

                    genus.map(_genus => {
                        let tmp_insect = []

                        insect.map(_insect => {
                            
                            if (_insect.fields.genus == _genus.pk)
                            
                                tmp_insect.push(_insect)
                        })
                        if (_genus.fields.family == _family.pk)
                            tmp_genus.push({"genus": _genus, "insect": tmp_insect})
                    })

                    if (_family.fields.order == _order.pk)
                        tmp_family.push({"family": _family, "genus": tmp_genus})
                })
                if (_order.fields.classes == _classes.pk)
                tmp_order.push({"order": _order, "family": tmp_family})
            })
            
            if (_classes.fields.phylum == _phylum.pk)
                tmp_classes.push({"classes": _classes, "order": tmp_order})
        })

        obj.phylum.push({"phylum": _phylum, "classes": tmp_classes})
    })
    
    
    let str = ``

    str += `<li>Kingdom: ` + obj.name;
    str += `<ul>`
    obj.phylum.map(_phylum => {
        str += `<li>Phylum: ` + _phylum.phylum.pk
        
        if (_phylum.classes.length > 0) {
            str += `<ul>`
            
            _phylum.classes.map(_classes => {
                str += `<li>Class: ` + _classes.classes.pk
        
                if (_classes.order.length > 0) {
                    str += `<ul>`
                    
                    _classes.order.map(_order => {
                        str += `<li>Order: ` + _order.order.pk
                        if (_order.family.length > 0) {
                            str += `<ul>`
                            
                            _order.family.map(_family => {
                                str += `<li>Family: ` + _family.family.pk
                                if (_family.genus.length > 0) {
                                    str += `<ul>`
                                    
                                    _family.genus.map(_genus => {
                                        str += `<li>Genus: ` + _genus.genus.pk
                                            
                                        if (_genus.insect.length > 0) {
                                            
                                            str += `<ul>`
                                            
                                            _genus.insect.map(_insect => {
                                                str += `<li><a href='/detail/`+ _insect.fields.slug +`'>insect: ` + _insect.pk + `</a></li>`
                                            })

                                            str += `</ul>`
                                        }

                                        str += `</li>`
                                    })

                                    str += `</ul>`
                                }

                                str += `</li>`
                            })

                            str += `</ul>`
                        }

                        str += `</li>`
                    })

                    str += `</ul>`
                }

                str += `</li>`
            })

            str += `</ul>`
        }

        str += `</li>`
    })

    str += `</ul>`
    str += `</li>`

    // kingdom.map(_kingdom => {
        
    //     str+= `<li>` + _kingdom.pk;
    //     str += `<ul>`
        
    //     str += `</ul>`
    //     str +=+`</li>`                
    // })
    
    $("#treeview").html(str)
}