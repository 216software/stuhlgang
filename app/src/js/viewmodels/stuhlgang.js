function Patient (data) {

    var self = this;
    self.type = "Patient";
    self.rootvm = data.rootvm;

    self.patient_number = ko.observable(data.patient_number);
    self.display_name = ko.observable(data.display_name);

    // I can draw my own link, thank you very much!
    self.my_url = ko.computed(function () {
        return `/patients/${self.patient_number()}`;
    });

};

export default Patient;
