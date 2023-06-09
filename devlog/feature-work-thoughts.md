06/08/2023

4:21 PM

Ahh... I'm kind of not feeling it but need to try

- [ ] use video recording with buffer stream
  - [ ] apply variance for auto focus
    - [ ] factor in pre-calibrated distances
      - [ ] check focuses regarding fstop
- [ ] fix audio recording
- [ ] restructure code to factor in voice control
- [ ] test at home for several minutes

4:28 PM

I feel like I can take the web stream code apart and pull the buffer part (what I want)

I've seen an example of picamera2 though with video recording where it had a buffer... hopefully it's not just for preview

4:42 PM

struggling...

4:54 PM

hmm... looks like audio recording is built into picamera2 will see, that would be convenient

looks like the boot script blocks camera access

5:01 PM

dumb... don't open YouTube distraction

hmm broken pipe tried recording sample with audio

still_during_video.py this could be something

5:07 PM

I feel like I should be able to take the web stream code and pull the server aspect out... write to USB instead (while intercepting frames in another thread)

hmm... maybe I do want to just pull frames out while recording not sure of performance

5:28 PM

I'm thinking something like this for the video recording autofocus control loop

<img src="./video-focus-control-loop.JPG"/>

there's the recording bit, then a sampling thread that's checking variance with access to stepper control (focus ring)

my variance algo sucked so I still have to come up with something for that

5:49 PM

ugh... something wrong with my usb drive status 32

will use gparted maybe...

I don't like this how the USB is problematic, it worked fine last time but that's a show stopper

Can't write to USB... can write to SD card but reduces life span

Ohh... I forgot you need sudo to use the USB drive... will write a try catch error message with that for a reminder

5:59 PM

just had a thought while I was having a snacky snack, there needs to be a variance interrupt thing while changing zoom levels eg. near/mid/far, so the focus zoom set for each of those ranges isn't interrupted

6:04 PM

installing opencv

weird that it's not on here already...

6:23 PM

distracted by PT2 not working

6:57 PM

man... I'm losing it, the drive, distracted by PT2, should not have looked at it

7:08 PM

okay... I do have an issue `capture_request` wants to write to a file but I want to have a buffer

I'll use the `capture_array` I think... then decode it into an img with opencv

7:30 PM

you are failing doctor... can't get this `np_array` to be read by cv for the variance check

7:44 PM

oh man I think I got it

7:57 PM

I should be able to do the auto focus and record bit here shortly

I'll do 3 samples (stepper values)

8:05 PM

ugh... this is where my code starts to get nasty

```
def start_sampling(self):
    while self.recording:
      prev_var = 0
      var_samples = []
      focus_far = True # first dir

      if (self.pause_autofocus != True):
        np_arr = self.camera.capture_array("lores")
        variance = self.get_variance(np_arr)
        
        if (prev_var == 0):
          prev_var = variance
        else:
          if (variance > prev_var):
            self.focus_stepper.focus_far(1)
          else:


      time.sleep(1)
```

this sampling/deciding which way to go then staying at the ideal focus

it will probably rarely ever just sit still

hmm I just realized something too, not sure of the speed I'm using on the steppers

looks like it's using `0.001` second per step and there are 8 of them

8:20 PM

seems like the 1s sampling is not fast enough

I will try for 24fps

8:25 PM

oof... my guy with the `sudo rm rf...` yikes

folders gone lol from `/home/pi`

VERSION CONTROL...

oh no... the OLED library is gone

oof

8:31 PM

yeah.......... everything's gone... good job Jacob

why did this happen? because I was moving video files from usb to sd for sftp to win 10 desktop

the files are written in root so can't delete them as pi, can change ownership

8:36 PM

I did realize the steppers have built in delay as they move

so far the auto focus is not working

ahh my old code was stepping in 5 increments

the time to move 25 steps is too short...

```
1686275244.2401679
1686275244.4660704
```

let's see...

it does only take 0.2 seconds hmm

let me time it a full rotation

oh  damn... I built in a focal length method into the stepper class huh

yeah... that seems right 2.8 seconds for 350 steps

8:57 PM

hmm... I wonder if the variance is bad because the image is bad

in the recorded video I see it getting better but the variance is not changing by much

9:02 PM

oh yeah these images are f'd lol

<img src="./broken.JPG"/>

So yeah... got the code to run but not working with right image... I had a suspicion since the answers were using greyscale

9:33 PM

just soldered up some new batteries for tomorrow

this variance thing needs work, I think I need to do major steps in some direction to get a large variance change then narrow it down

based on the initial settings