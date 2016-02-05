
def is_network_busy(event_threshold=4):
    import datetime
    activity_threshold = event_threshold * 4
    activity_dtime = datetime.timedelta(minutes = activity_threshold)
    event_dtime = datetime.timedelta(minutes = event_threshold)

    import knowledge
    device_db = knowledge.load_db()

    recent_device_ids = []
    recent_device_dts = []

    most_recent_id = -1
    most_recent_dt = -1

    for id,d in enumerate(device_db):
        #print(d.time_since_last_occurance())

        dt_since_last_visit = d.time_since_last_occurance()

        if dt_since_last_visit < activity_dtime:
            recent_device_ids.append(id)
            recent_device_dts.append(dt_since_last_visit)

            # store the most recent device id and delta time
            if most_recent_dt == -1:
                most_recent_id = id
                most_recent_dt = dt_since_last_visit
            elif dt_since_last_visit < most_recent_dt:
                most_recent_id = id
                most_recent_dt = dt_since_last_visit

    if len(recent_device_ids) == 0:
        print("Found ZERO active devices on the network - this seems suspicious.")
        # assuming there is at least one constant device always available (e.g. the router)
        return False

    #if len(recent_device_ids) > 0:
    #    print("Found "+str(len(recent_device_ids))+" (recently) active devices on network.")

    now_active_device_ids = []
    now_active_device_dts = []
    now_inactive_device_ids = []
    now_inactive_device_dts = []

    for id,dt in zip(recent_device_ids,recent_device_dts):
        d = device_db[id]

        # let's look at the relative availability
        #has someone recently become inactive?
        if (dt - most_recent_dt) > event_dtime:
            print(d._name+" has been inactive for a while now ...")
            # MAYBE IT IS OK TO USE THE NETWORK NOW ?
            now_inactive_device_ids.append(id)
            now_inactive_device_dts.append(dt)
        else:
            # check if these have only recently become active ...
            now_active_device_ids.append(id)
            now_active_device_dts.append(dt)

    # now let's look into the history of availability a little more
