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

