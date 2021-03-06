#vim: set expandtab ts=4 sw=4 filetype=python:

import datetime
import logging

from stuhlgang.webapp.framework.handler import Handler
from stuhlgang.webapp.framework.response import Response
from stuhlgang import pg

log = logging.getLogger(__name__)

# TODO: for now, do not comment these out or remove them.  Later, move
# these into the dashboard handlers,  because they're the only folks
# that are using them.
module_template_prefix = 'stuhlgang'
module_template_package = 'stuhlgang.webapp.stuhlgang.templates'

class Splash(Handler):

    route_strings = set(['GET /'])
    route = Handler.check_route_strings

    @Handler.require_json
    def handle(self, req):

        return Response.json(dict(
            message="Welcome to the StuhlGang API",
            success=True,
            reply_timestamp=datetime.datetime.now()))

class PatientsForCaretaker(Handler):

    route_strings = set([
        "GET /api/patients-for-caretaker",
    ])

    route = Handler.check_route_strings

    @Handler.get_session_from_cookie_or_json_or_QS
    def handle(self, req):

        offset = int(req.wz_req.args.get("offset", 0))
        limit = int(req.wz_req.args.get("offset", 10))

        patients = list(pg.patients.Patient.patients_for_caretaker(
            self.cw.get_pgconn(),
            req.user.person_uuid,
            offset,
            limit))

        return Response.json(dict(
            success=True,
            message="Retrieved {0} patients".format(len(patients)),
            reply_timestamp=datetime.datetime.now(),
            offset=offset,
            limit=limit,
            patients=patients))

class OnePatientForCaretaker(Handler):

    route_strings = set([
        "GET /api/one-patient-for-caretaker",
        "GET /api/patient",
    ])

    route = Handler.check_route_strings

    @Handler.get_session_from_cookie_or_json_or_QS
    def handle(self, req):

        verified_caretaker = pg.patients.Patient.verify_is_my_caretaker(
            self.cw.get_pgconn(),
            req.wz_req.args["patient_number"],
            req.user.person_uuid)

        if not verified_caretaker:

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, you're not a caretaker for patient {patient_number}!".format(**req.wz_req.args)))

        else:

            patient = pg.patients.Patient.by_patient_number(
                self.cw.get_pgconn(),
                req.wz_req.args["patient_number"])

            return Response.json(dict(
                success=True,
                message="Retrieved {0}.".format(patient.display_name),
                reply_timestamp=datetime.datetime.now(),
                patient=patient))

class AddPatientForCaretaker(Handler):

    route_strings = set([
        "POST /api/add-patient-for-caretaker",
    ])

    route = Handler.check_route_strings

    required_json_keys = [
        "display_name",
        "extra_notes",
        "extra_data"
    ]

    @Handler.get_session_from_cookie_or_json_or_QS
    @Handler.require_json
    def handle(self, req):

        new_patient = pg.patients.Patient.insert(
            self.cw.get_pgconn(),
            req.json["display_name"],
            req.json["extra_notes"],
            req.json["extra_data"])

        link = pg.patients.Patient.link_to_caretaker(
            self.cw.get_pgconn(),
            new_patient.patient_number,
            req.user.person_uuid,
            None,
            None)

        return Response.json(dict(
            success=True,
            reply_timestamp=datetime.datetime.now(),
            message="Stored patient {0}!".format(new_patient.display_name),
            new_patient=new_patient,
            link=link))

class StorePatientEvent(Handler):

    route_strings = set([
        "POST /api/store-patient-event",
    ])

    route = Handler.check_route_strings

    required_json_keys = [
        "patient_number",
        "event_timestamp",
        "extra_notes",
        "extra_data"
    ]

    @Handler.get_session_from_cookie_or_json_or_QS
    @Handler.require_json
    def handle(self, req):

        verified_caretaker = pg.patients.Patient.verify_is_my_caretaker(
            self.cw.get_pgconn(),
            req.json["patient_number"],
            req.user.person_uuid)

        if not verified_caretaker:

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, you're not a caretaker for patient {patient_number}!".format(**req.json)))

        else:

            pe = pg.patients.PatientEvent.insert(
                self.cw.get_pgconn(),
                req.json["patient_number"],
                req.json["event_timestamp"],
                req.user.person_uuid,
                req.json["extra_notes"],
                req.json["extra_data"])

            return Response.json(dict(
                success=True,
                reply_timestamp=datetime.datetime.now(),
                message="Stored patient event {0}!".format(pe.patient_event_number),
                patient_event=pe))

class PatientEvents(Handler):

    route_strings = set([
        "GET /api/patient-events",
    ])

    route = Handler.check_route_strings

    @Handler.get_session_from_cookie_or_json_or_QS
    def handle(self, req):

        verified_caretaker = pg.patients.Patient.verify_is_my_caretaker(
            self.cw.get_pgconn(),
            req.wz_req.args["patient_number"],
            req.user.person_uuid)

        if not verified_caretaker:

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, you're not a caretaker for patient {patient_number}!".format(**req.wz_req.args)))

        else:

            offset = int(req.wz_req.args.get("offset", 0))
            limit = int(req.wz_req.args.get("limit", 10))

            patient_events = list(pg.patients.PatientEvent.by_patient_number(
                self.cw.get_pgconn(),
                req.wz_req.args["patient_number"],
                offset,
                limit))

            total_event_count = pg.patients.PatientEvent.count_patient_events(
                self.cw.get_pgconn(),
                req.wz_req.args["patient_number"])

            return Response.json(dict(
                success=True,
                message="Retrieved {0} events of {1} total.".format(
                    len(patient_events),
                    total_event_count),
                reply_timestamp=datetime.datetime.now(),
                offset=offset,
                limit=limit,
                patient_events=patient_events,
                total_event_count=total_event_count))

class OnePatientEvent(Handler):

    route_strings = set([
        "GET /api/patient-event",
    ])

    route = Handler.check_route_strings

    @Handler.get_session_from_cookie_or_json_or_QS
    def handle(self, req):

        try:
            pe = pg.patients.PatientEvent.by_patient_event_number(
                self.cw.get_pgconn(),
                req.wz_req.args["patient_event_number"])

        except KeyError as ex:

            log.error(ex)

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message=ex.args[0]))

        else:

            verified_caretaker = pg.patients.Patient.verify_is_my_caretaker(
                self.cw.get_pgconn(),
                pe.patient_number,
                req.user.person_uuid)

            if not verified_caretaker:

                return Response.json(dict(
                    success=False,
                    reply_timestamp=datetime.datetime.now(),
                    message="Sorry, you're not a caretaker for patient {0}!".format(
                        pe.patient_number)))

            else:

                return Response.json(dict(
                    success=True,

                    message="Retrieved patient event {0}.".format(
                        pe.patient_event_number),

                    reply_timestamp=datetime.datetime.now(),
                    patient_event=pe))

class DeletePatient(Handler):

    route_strings = set([
        "POST /api/delete-patient",
        "DELETE /api/patient",
    ])

    required_json_keys = [
        "patient_number",
    ]

    route = Handler.check_route_strings

    @Handler.get_session_from_cookie_or_json_or_QS
    def handle(self, req):

        verified_caretaker = pg.patients.Patient.verify_is_my_caretaker(
            self.cw.get_pgconn(),
            req.json["patient_number"],
            req.user.person_uuid)

        if not verified_caretaker:

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, you're not a caretaker for patient {patient_number}!".format(**req.json)))

        else:

            deleted_patient = pg.patients.Patient.delete_patient(
                self.cw.get_pgconn(),
                req.json["patient_number"])

            return Response.json(dict(
                deleted_patient=deleted_patient,
                success=True,
                reply_timestamp=datetime.datetime.now(),
                message="Deleted patient {0}!".format(req.json["patient_number"])))


class DeletePatientEvent(Handler):

    route_strings = set([
        "POST /api/delete-patient-event",
        "DELETE /api/patient-event",
    ])

    route = Handler.check_route_strings

    required_json_keys = [
        "patient_event_number",
    ]

    @Handler.get_session_from_cookie_or_json_or_QS
    def handle(self, req):

        try:
            pe = pg.patients.PatientEvent.by_patient_event_number(
                self.cw.get_pgconn(),
                req.json["patient_event_number"])

        except KeyError as ex:

            log.error(ex)

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message=ex.args[0]))

        else:

            verified_caretaker = pg.patients.Patient.verify_is_my_caretaker(
                self.cw.get_pgconn(),
                pe.patient_number,
                req.user.person_uuid)

        if not verified_caretaker:

            return Response.json(dict(
                success=False,
                reply_timestamp=datetime.datetime.now(),
                message="Sorry, you're not a caretaker for patient {0}!".format(pe.patient_number)))

        else:

            deleted_patient_event = pg.patients.PatientEvent.delete_patient_event(
                self.cw.get_pgconn(),
                req.json["patient_event_number"])

            return Response.json(dict(
                deleted_patient_event=deleted_patient_event,
                success=True,
                reply_timestamp=datetime.datetime.now(),
                message="Deleted patient event {0}!".format(req.json["patient_event_number"])))

