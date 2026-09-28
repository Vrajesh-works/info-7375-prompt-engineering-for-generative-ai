# Root.tsx registration for this video

A fresh `brutalist.art` clone does not register the six components this video uses.
After copying `DerivationScenes.tsx.txt` into `runtime/remotion/src/scenes/` as
`DerivationScenes.tsx`, add these
two blocks to `runtime/remotion/src/Root.tsx`, then run `./art scene-index`.

**1. With the other imports at the top of the file:**

```tsx
import {
  ScaleAnchorCard, scaleAnchorCardSchema,
  DerivationLadder, derivationLadderSchema,
  AssumptionFan, assumptionFanSchema,
  SurvivingClaim, survivingClaimSchema,
  ClaimAudit, claimAuditSchema,
  BoundaryCard, boundaryCardSchema,
} from './scenes/DerivationScenes';
```

**2. Inside the `<>` … `</>` list of `<Composition>` elements:**

```tsx
      {/* ── claude-liam — derivation / hidden-parameter illustrations (INFO 7375) ── */}
      <Composition id="ScaleAnchorCard" component={ScaleAnchorCard}
        durationInFrames={240} fps={30} width={1920} height={1080}
        schema={scaleAnchorCardSchema} defaultProps={scaleAnchorCardSchema.parse({})} />
      <Composition id="DerivationLadder" component={DerivationLadder}
        durationInFrames={240} fps={30} width={1920} height={1080}
        schema={derivationLadderSchema} defaultProps={derivationLadderSchema.parse({})} />
      <Composition id="AssumptionFan" component={AssumptionFan}
        durationInFrames={240} fps={30} width={1920} height={1080}
        schema={assumptionFanSchema} defaultProps={assumptionFanSchema.parse({})} />
      <Composition id="SurvivingClaim" component={SurvivingClaim}
        durationInFrames={240} fps={30} width={1920} height={1080}
        schema={survivingClaimSchema} defaultProps={survivingClaimSchema.parse({})} />
      <Composition id="ClaimAudit" component={ClaimAudit}
        durationInFrames={240} fps={30} width={1920} height={1080}
        schema={claimAuditSchema} defaultProps={claimAuditSchema.parse({})} />
      <Composition id="BoundaryCard" component={BoundaryCard}
        durationInFrames={240} fps={30} width={1920} height={1080}
        schema={boundaryCardSchema} defaultProps={boundaryCardSchema.parse({})} />
```
