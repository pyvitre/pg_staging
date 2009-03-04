##
## Staging Class to organise processing
##

import os

from options import VERBOSE, DRY_RUN
import pgbouncer, restore

class Staging:
    """ Staging Object relates to a database name, where to find the backups
    and a destination where to restore it"""

    def __init__(self,
                 dbname,
                 backup_host,
                 backup_base_url,
                 backup_date,
                 host,
                 postgres_port,
                 pgbouncer_port,
                 pgbouncer_conf,
                 pgbouncer_rcmd,
                 keep_bases  = 2,
                 auto_switch = True,
                 use_sudo    = True):
        """ Create a new staging object, configured """

        self.dbname          = dbname
        self.backup_host     = backup_host
        self.backup_base_url = backup_base_url
        self.backup_date     = backup_date
        self.host            = host
        self.postgres_port   = postgres_port
        self.pgbouncer_port  = pgbouncer_port
        self.pgbouncer_conf  = pgbouncer_conf
        self.pgbouncer_rcmd  = pgbouncer_rcmd
        self.keep_bases      = keep_bases
        self.auto_switch     = auto_switch
        self.use_sudo        = use_sudo

        self.backup_filename = "%s%s.%s.dump" \
                               % (backup_base_url, dbname, backup_date)

        if VERBOSE:
            print "backup filename is '%s'" % self.backup_filename

    def get_dump(self):
        """ get the dump file from the given URL """
        import tempfile, httplib

        tmp_prefix = "%s.%s." % (self.dbname, self.backup_date)

        dump_fd, filename = tempfile.mkstemp(suffix = ".dump",
                                             prefix = tmp_prefix)

        conn = httplib.HTTPConnection(self.backup_host)
        conn.request("GET", self.backup_filename)
        r = conn.getresponse()

        if r.status != 200:
            raise CouldNotGetDumpException, r.reason

        os.write(dump_fd, r.read())

        # FIXME: get the file content
        return dump_fd, filename

    def restore(self):
        """ launch a pg_restore for the current staging configuration """

        # first, download the dump we need.
        dump_fd, filename = self.get_dump()

        if VERBOSE:
            print "Got the dump in '%s'" % filename
            os.system("ls -l %s" % filename)

        if VERBOSE:
            print "Removing the dump file '%s'" % filename

        os.close(dump_fd)
        os.unlink(filename)

        raise NotYetImplementedException

    def switch(self):
        """ edit pgbouncer configuration file to have canonical dbname point
        to given date (backup_date) """
        pass

    def drop(self):
        """ drop the given database: dbname_%(backup_date) """
        pass


class NotYetImplementedException(Exception):
    """ Please try again """
    pass

class CouldNotGetDumpException(Exception):
    """ HTTP Return code was not 200 """
    pass