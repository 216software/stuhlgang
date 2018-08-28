import ko from 'knockout';
import BasePage from './BasePage';
import Patient from './stuhlgang';

class Dashboard extends BasePage {
  constructor () {
    super();

    this.patients = ko.observableArray([

        ko.utils.arrayMap(

            // This is the data you'll get back from an AJAX query.
            {
                "limit": 10,
                "message": "Retrieved 1 patients",
                "offset": 0,
                "patients": [
                    {
                    "display_name": "Charlie",
                    "extra_data": {
                        "birthdate": "2005-04-06"
                    },
                    "extra_notes": "does not complain of being constipated",
                    "inserted": "2018-08-27T14:24:22.403500-04:00",
                    "patient_number": 58,
                    "updated": null
                    }
                ],
                "reply_timestamp": "2018-08-28T11:56:57.773839",
                "success": true
            },

            function (x) {
                x.rootvm = "EVAN THIS IS WHERE I PASS A REFERENCE TO THE TOP VIEW MODEL";
                return new Patient(x);

            })

    ]);

    /*
      {

        id: 1,
        name: 'Billy Billson',
      },
      {
        id: 2,
        name: 'Johnny Johnson',
      },
    ]);
    */

    // This is a job for the Patient!
    this.patientUrl = ({ id }) => ko.computed(() => `/patients/${id}`, this);

  }


    // Just personal preference, but I would just do the
    // patients().length > 0 test inside the HTML, so that there's no
    // doubt about how it works.
  isEmpty () {
    return !!(this.patients().length === 0);
  }
}

export default Dashboard;
