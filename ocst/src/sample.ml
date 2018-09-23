open System
open BatEnum

let shift=3600*7

let sample seed swf_out swf_in  =
  let jt,mp = Io.parse_jobs swf_in
  in let () = Random.init seed
  in let forward_shifted_users,backward_shifted_users = 
    let f i j (l,l') = match Random.int 5 with
      |1 -> (l@[j.u],l')
      |2 -> (l,l'@[j.u])
      |_ -> (l,l')
    in Hashtbl.fold f jt ([],[])
  in let printer chan = 
     let f i j = 
       let predicate u' u = u = u'
       in if List.exists (predicate j.u) forward_shifted_users then
         Io.printjob_shift (j.r+shift) (Hashtbl.find jt i) i chan
       else if List.exists (predicate j.u) backward_shifted_users then
         Io.printjob_shift (j.r-shift) (Hashtbl.find jt i) i chan
       else
         Io.printjob_shift j.r j i chan
     in Hashtbl.iter f jt
  in Io.wrap_io_out (Some swf_out) printer
