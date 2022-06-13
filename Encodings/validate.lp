

conflict(0, RID, RID', NID, T) :- robot_at(RID ,NID, T), robot_at(RID', NID, T), RID < RID'.
conflict(1, RID, RID', (NID, NID'), T) :- robot_at(RID, NID, T), robot_at(RID, NID', T+1), robot_at(RID', NID', T), robot_at(RID', NID, T+1), RID < RID'.
min_conflict(CID, RID, RID', NID, T) :- conflict(CID, RID, RID', NID, T), #false : conflict(_, _, _, _, T'), T' < T.
