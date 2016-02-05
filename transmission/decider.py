
def is_network_busy(event_threshold=4):
    import datetime
    activity_threshold = event_threshold * 4
    activity_dtime = datetime.timedelta(minutes = activity_threshold)
    event_dtime = datetime.timedelta(minutes = event_threshold)

    import knowledge
    device_db = knowledge.load_db()

    recent_device_ids = []
    recent_device_dts = []
    invisible_device_ids = []
    invisible_device_dts = []

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

        else:
            # these are devices that have long been gone from our view
            invisible_device_ids.append(id)
            invisible_device_dts.append(dt_since_last_visit)

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
            print(d._name+" has just become inactive ...")
            # MAYBE IT IS OK TO USE THE NETWORK NOW ?
            now_inactive_device_ids.append(id)
            now_inactive_device_dts.append(dt)
            d.set_priority(0)
        else:
            print(d._name+" is active right now ...")
            # TODO: check if these have only recently become active ...?
            now_active_device_ids.append(id)
            now_active_device_dts.append(dt)
            d.set_priority(-1)

    # TODO: let's look into the history of availability a little more
    # NOTE: but maybe keep it simple and not overly complicate things ?

    for id,dt in zip(invisible_device_ids,invisible_device_dts):
        d = device_db[id]

        if (dt-most_recent_dt) > activity_dtime * 4:
            print(d._name+" has been invisible for a long time")
            # very high priority device (make network resources available in case of return)
            d.set_priority(1)
        else:
            print(d._name+" has been invisible for a while")
            d.set_priority(0)


    return True
