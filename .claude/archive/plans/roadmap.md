# NBA Prediction App - Development Roadmap

**Timeline:** 9 weeks to MVP (Personal Use)
**Start Date:** November 1, 2024
**MVP Target:** January 3, 2025
**Public Launch Target:** February 2025

## Phase 0: Refactor & Cleanup (Week 1)
**Deadline:** November 8, 2024

### Critical Codebase Cleanup
**Deliverables:**
- Remove all duplicate files and directories
- Consolidate data transformation logic
- Fix technical debt from codebase status report
- Establish clean architecture foundation
- Update documentation to reflect current state

**Tasks:**
1. Delete duplicate files:
   - Remove `src/utils/extractor copy.ts`
   - Remove `src/data copy/` directory
   - Verify no other duplicates exist
2. Refactor data transformation:
   - Consolidate `mapper.ts` and extraction utilities
   - Create single source of truth for stat transformations
   - Remove redundant transformation logic
3. Clean up data files:
   - Move all sample data to `src/data/sample-data/`
   - Verify sample data structure matches README
   - Remove unused JSON files
4. Code quality improvements:
   - Fix any lingering TypeScript errors
   - Add missing type definitions
   - Ensure consistent naming conventions
5. Documentation updates:
   - Update CLAUDE.md with current architecture
   - Verify all file paths in docs are correct
   - Add inline code comments where needed

**Success Metrics:**
- Zero duplicate files in codebase
- All data in correct directories
- No TypeScript compilation errors
- Documentation matches current state
- Clean git status (all staged changes committed)

**Risks:**
- Breaking existing functionality during refactor
- Discovering additional technical debt

**Mitigation:**
- Write tests before refactoring critical paths
- Commit frequently with descriptive messages
- Keep refactor scope limited to cleanup only

## Phase 1: Foundation & Integration (Weeks 2-3)
**Deadline:** November 22, 2024

### Week 2: Core Integration
**Deliverables:**
- Connect prediction formulas to live NBA data
- Create data transformation pipeline from API to formulas
- Implement basic caching strategy (6-hour cache)
- Initial prediction engine working

**Tasks:**
1. Create `PredictionService` to bridge data fetching and formulas
2. Implement `TeamStatsTransformer` for API data to formula inputs
3. Add localStorage caching layer for team stats
4. Wire up all 5 moneyline models to live data
5. Write integration tests for data flow

**Dependencies:**
- Phase 0 refactor complete
- Clean codebase foundation

**Success Metrics:**
- Live predictions generating for today's games
- All 5 moneyline models producing probabilities
- Cache hit rate > 80% for repeated requests
- Integration tests passing

### Week 3: Prediction UI Implementation
**Deliverables:**
- Functional prediction detail page
- Model breakdown display component
- Confidence scoring visualization
- Basic EV/ROI indicators

**Tasks:**
1. Build `/pre-game/prediction/[gameId]` page
2. Create `ModelBreakdown` component showing all 5 models
3. Implement `ConfidenceIndicator` (High/Medium/Low)
4. Add `ValueBadge` for positive EV games
5. Connect pre-game cards to prediction pages

**Dependencies:**
- Week 2 data integration complete
- Sample odds data for EV calculations

**Risks:**
- API rate limiting during development
- Model disagreement handling complexity

## Phase 2: Situational Adjustments & Betting Features (Weeks 4-5)
**Deadline:** December 6, 2024

### Week 4: Situational Adjustments
**Deliverables:**
- Rest days detection from schedule
- Back-to-back game identification
- Recent form calculations (last 10 games)
- Home/away performance splits

**Tasks:**
1. Implement `ScheduleAnalyzer` for rest/B2B detection
2. Create `FormCalculator` using last N games API
3. Add home/away split fetching to `StatsClient`
4. Update prediction formulas with adjustment weights
5. Manual injury impact UI (text input initially)

**Success Metrics:**
- All 12 situational adjustments factored into predictions
- Prediction accuracy baseline established
- Form adjustments changing probabilities by 5-15%

### Week 5: Betting Odds Integration
**Deliverables:**
- Manual odds input interface
- Moneyline odds comparison page
- Kelly Criterion bet sizing calculator
- Value bet highlighting system

**Tasks:**
1. Create `OddsInputModal` for manual entry
2. Build `/pre-game/betting-odds/moneyline` page
3. Implement `KellyCalculator` component
4. Add `ValueBetFilter` to game list
5. Create `BankrollManager` with localStorage

**Dependencies:**
- Prediction engine fully functional
- EV/ROI calculations validated

**Risks:**
- Manual odds entry friction
- Kelly sizing too aggressive for users

## Phase 3: MVP Features & Testing (Weeks 6-7)
**Deadline:** December 20, 2024

### Week 6: Bet Tracking & Analytics
**Deliverables:**
- Bet history tracking system
- Performance dashboard
- ROI tracking over time
- Win rate by confidence level

**Tasks:**
1. Create `BetTracker` service with localStorage
2. Build `/analytics` dashboard page
3. Implement `PerformanceChart` components
4. Add CSV export for bet history
5. Create `AccuracyValidator` for model testing

**Success Metrics:**
- 100% of predictions logged automatically
- Historical performance visible
- ROI calculation accurate to penny
- Export functionality working

### Week 7: Testing & Refinement
**Deliverables:**
- 50%+ test coverage
- E2E tests for critical paths
- Performance optimizations
- Mobile responsive fixes

**Tasks:**
1. Write unit tests for all formulas
2. Create E2E tests for prediction flow
3. Add loading states and error boundaries
4. Optimize bundle size (code splitting)
5. Fix mobile layout issues

**Dependencies:**
- All MVP features complete
- Test data available

**Risks:**
- Test coverage revealing bugs
- Performance issues with large datasets

## Phase 4: Polish & Launch Prep (Weeks 8-9)
**Deadline:** January 3, 2025

### Week 8: Live Features & Polish
**Deliverables:**
- Basic live game tracking
- Real-time score updates
- Live win probability updates
- Documentation complete

**Tasks:**
1. Implement `LiveGameTracker` with polling
2. Create live scoreboard component
3. Add win probability chart
4. Write user documentation
5. Create formula methodology docs

**Success Metrics:**
- Live scores updating every 30 seconds
- Win probability adjusting with score
- Documentation covers all features

### Week 9: Deployment & Validation
**Deliverables:**
- Production deployment
- Monitoring setup
- Beta testing feedback
- Bug fixes from testing

**Tasks:**
1. Deploy to Vercel/production
2. Setup error monitoring (Sentry)
3. Configure analytics (GA4/Mixpanel)
4. Run 7-day beta test
5. Fix critical bugs

**Dependencies:**
- All features tested
- Production environment ready

**Risks:**
- Production API limits different
- Deployment configuration issues

## Success Metrics for MVP

### Technical Metrics
- Page load time < 2 seconds
- Prediction generation < 2 seconds
- 50%+ test coverage
- Zero critical bugs
- 99% uptime

### Product Metrics
- All 5 moneyline models functional
- 12 situational adjustments applied
- EV/ROI calculations accurate
- Bet tracking persistent
- Mobile responsive

### Business Metrics
- Daily predictions for all games
- Positive EV identification working
- Kelly sizing recommendations
- Historical tracking enabled
- Documentation complete

## Post-MVP Phases (January - April 2025)

### Phase 5: Spread Predictions (Weeks 10-13)
**Target:** January 31, 2025

- Implement 10 spread models
- Add spread-specific adjustments
- Create spread betting UI
- Validate cover probability calculations

### Phase 6: Over/Under Predictions (Weeks 14-17)
**Target:** February 28, 2025

- Implement 9 total models
- Add volatility analysis
- Create O/U betting interface
- Historical O/U tracking

### Phase 7: Advanced Features (Weeks 18-21)
**Target:** March 28, 2025

- Live odds API integration
- Real-time value alerts
- Advanced analytics dashboard
- Lineup change detection
- Referee tendency analysis

### Phase 8: Monetization Prep (Weeks 22-25)
**Target:** April 25, 2025

- User authentication system
- Subscription management
- Payment processing
- Pick delivery system
- Admin dashboard

## Risk Mitigation Strategy

### High-Risk Items
1. **NBA API Rate Limits**
   - Mitigation: Aggressive caching, sample data fallback

2. **Prediction Accuracy < 55%**
   - Mitigation: Model refinement period, A/B testing

3. **Live Odds Integration**
   - Mitigation: Manual entry MVP, paid API research

4. **Injury Data Availability**
   - Mitigation: Manual input UI, web scraping backup

### Dependencies
- NBA.com API availability
- Sample data accuracy
- Formula correctness
- UI component library stability

## Immediate Next Steps (Week 1 - Refactor Phase)

1. **Day 1:** Remove duplicate files and directories
2. **Day 2:** Consolidate data transformation logic
3. **Day 3:** Clean up data files and move to correct locations
4. **Day 4:** Fix TypeScript errors and add type definitions
5. **Day 5:** Update documentation to match current state
6. **Weekend:** Review changes, commit cleanup work

## Resource Requirements

### Development
- 1 full-stack developer (40 hrs/week)
- NBA League Pass (for validation)
- Production hosting (Vercel)
- Error monitoring (Sentry free tier)

### Data
- NBA.com API access (free)
- Manual odds entry (initially)
- Sample data for testing
- Historical games for validation

## Definition of Done for MVP

### Must Have (Week 9)
- All 5 moneyline models working
- Live data integration complete
- Prediction detail pages functional
- Basic bet tracking implemented
- EV/ROI calculations accurate
- Mobile responsive design
- 50% test coverage
- Production deployed

### Nice to Have (Post-MVP)
- Spread predictions
- Over/under predictions
- Live odds integration
- Advanced analytics
- User accounts
- Payment system

## Conclusion

This roadmap delivers a functional MVP in 9 weeks (1 week refactor + 8 weeks development) focusing on moneyline predictions with manual odds entry. The foundation is strong with completed formulas and data fetching. Critical path starts with codebase cleanup, followed by UI integration and situational adjustments. Post-MVP phases add spread/totals and monetization features over the following 4 months.

**Key Success Factor:** Starting with a clean refactored codebase ensures solid foundation. Maintaining focus on moneyline MVP before expanding to additional bet types. Daily progress on integration work in Weeks 2-3 sets foundation for remaining features.
