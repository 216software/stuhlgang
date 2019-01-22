import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'pagerjs';

import StuhlgangViewModel from './viewmodels/stuhlgangviewmodel';

var sgvm;

$(document).ready(function () {
    sgvm = new StuhlgangViewModel();

    console.log(ko);
    console.log(pager);

    pager.extendWithPage(sgvm);
    ko.applyBindings(sgvm);
    pager.start();

    console.log("Whoomp there it is!");

});
