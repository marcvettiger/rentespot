import threading





class downloadthread(threading.thread):
    def __init__(self, thread_id, chunk):
        threading.thread.__init__(self)
        self.thread_id = thread_id
        self.chunk = chunk

    def run(self):
        logger.info("starting thread %s" % self.thread_id)
        res = dataengine().get_update_data(self.chunk)
        logger.info("exiting thread %s" % self.thread_id)


def multithreaded_download():
    """multithread function to download new forecast data from msw."""
    spread_name = "rentepointdb"
    logger.info("starting multi threaded download")

    ids = spots().get_ids()

    chunk_size = 100
    logger.info("slicing list in even size chunks of %s" % chunk_size)
    chunks = [ids[i:i + chunk_size] for i in xrange(0, len(ids), chunk_size)]
    logger.debug("number of chunks: %s" % len(chunks))

    threads = []

    for i in range(0, len(chunks[:5])):
        thread = downloadthread(i, chunks[i])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    print "exiting main thread"
    logger.info("finished application")


if __name__ == '__main__':
    logging.config.fileConfig('cfg/logger.conf')
    logger = logging.getLogger()