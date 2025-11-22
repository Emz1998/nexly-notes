# NBA Prediction App - Product Requirements Document

## Product Overview

**Vision:** Build a traditional statistical model-based NBA prediction app that identifies profitable betting opportunities through mathematical analysis and value detection.

**Purpose:** Personal entertainment and sports analytics tool with potential to monetize through pick selling once prediction accuracy is validated.

**Core Value Proposition:**

- Data-driven NBA game predictions using multiple statistical models
- Positive Expected Value (EV) identification for profitable betting
- Transparent model breakdowns showing prediction confidence
- Pure statistical approach using NBA.com official data

## Goals and Success Metrics

**Primary Success Metrics:**

- Prediction accuracy of 55% or higher on moneyline picks
- Positive EV identification rate of 60% or higher
- ROI tracking showing profitable betting strategy

**Secondary Success Metrics:**

- Model consensus agreement rate (higher agreement = higher confidence)
- Accuracy by confidence level (high-confidence picks should be more accurate)
- Long-term profitability when following Kelly Criterion bet sizing

**Future Monetization Metrics:**

- Pick conversion rate (free users to paid subscribers)
- Subscriber retention rate
- Accuracy transparency builds credibility

## User Personas

**Phase 1 - Personal Use:**

- **You:** Sports analytics enthusiast testing prediction models
- **Use Case:** Daily NBA game analysis, value betting identification, model refinement
- **Needs:** Clean predictions, model transparency, EV calculations, simple interface

**Phase 2 - Monetization:**

- **Serious Bettors:** Looking for data-driven edge with proven accuracy
- **Casual Bettors:** Want simple win/loss predictions with confidence scores
- **Sports Analysts:** Interested in statistical models and methodology

## MVP Features - Phase 1 (Moneyline Only)

### Core Prediction Engine

**Five Statistical Models:**

1. **ELO Rating Model** - Team strength differential with home court advantage
2. **Net Rating Model** - Offensive vs defensive efficiency matchup
3. **Pythagorean Expectation** - Win probability based on scoring patterns
4. **Four Factors Model** - Weighted analysis (Shooting, Turnovers, Rebounding, FT)
5. **Pace-Adjusted Model** - Tempo-adjusted efficiency ratings

**Twelve Situational Adjustments:**

- Recent form (last 10 games win percentage)
- Rest days and back-to-back game fatigue
- Travel distance and time zone effects
- Injury impact (manual input initially)
- Head-to-head historical matchups
- Strength of schedule adjustments
- Clutch performance metrics
- Current winning/losing streaks
- Home court venue strength
- Pace matchup advantages
- Denver altitude factor
- Conference strength differentials

**Value Calculations:**

- Convert model outputs to win probabilities
- Compare to market odds (manual input initially)
- Calculate Expected Value (EV) and ROI
- Kelly Criterion optimal bet sizing
- Fractional Kelly for risk management

### Data Pipeline

**NBA.com API Integration:**

- Daily fetch of team statistics (Base, Advanced, Four Factors)
- Season-to-date stats and rankings
- Last 10 games recent form data
- Home/Away splits
- Conference and division standings

**Stats Extraction:**

- Use existing stats-client.ts for API calls
- Use extract-stats.ts for field extraction
- Cache daily to minimize API calls
- Manual data entry for injuries and rest days initially

### User Interface Requirements

**Game Selection Page:**

- List of today's NBA games
- Team names, logos, records
- Game time and venue
- Filter by conference or specific teams

**Prediction Display:**

- Predicted winner with win probability percentage
- Confidence level (High/Medium/Low based on model consensus)
- Model breakdown showing each model's prediction
- Situational adjustments applied
- EV calculation if odds provided
- Kelly Criterion suggested bet size

**Value Identification:**

- Highlight games with positive EV in green
- Show expected value percentage
- Display required odds for break-even
- Clear "Value Bet" indicator

**Model Transparency:**

- Show individual model predictions
- Display situational adjustment impacts
- Explain confidence scoring methodology
- Link to documentation on how models work

### Technical Requirements

**Frontend:**

- Next.js 16 App Router
- React 19 with TypeScript
- Tailwind CSS v4 for styling
- Mobile-responsive design

**Backend/Data:**

- stats-client.ts for NBA API fetching
- extract-stats.ts for data extraction
- Formula files in src/lib/formulas/moneyline/
- Daily cron job for stats updates

**Prediction Generation:**

- Run all five models for each game
- Apply situational adjustments
- Calculate weighted consensus prediction
- Generate confidence scores
- Compute EV and Kelly sizing

**Performance:**

- Predictions generated in under 2 seconds per game
- Cache predictions for 6 hours
- Update when new data available

## Future Enhancements - Phase 2-3

### Spread Predictions (Phase 2)

**Ten Spread Models:**

- ELO Spread, Net Rating Spread, Pythagorean Spread
- Four Factors Spread, Pace-Adjusted Spread
- Off/Def Rating Spread, Moving Average Spread
- Market Consensus Spread, SOS Spread, Regression Spread

**Fifteen Situational Adjustments:**

- All moneyline adjustments plus spread-specific factors
- ATS (Against The Spread) recent form
- Blowout tendency analysis
- Garbage time effects
- Lineup change impacts

**Cover Probability:**

- Normal distribution analysis
- Standard deviation calculations
- Cover percentage for various spreads

### Over/Under Predictions (Phase 3)

**Nine Total Models:**

- Pace-Based Total, Off/Def Rating Total
- Simple Average Total, Four Factors Total
- Regression Total, Recent Form Total
- H2H Historical Total, Market Consensus
- Possessions-Based Total (most accurate)

**Fifteen Situational Adjustments:**

- Pace matchups, injury scoring impact
- Defensive matchup strength
- 3-point volume and variance
- Game stakes and motivation
- Referee tendencies

**Volatility Analysis:**

- Game-specific standard deviation
- Over/under hit probability
- Market movement signals

### Real-Time Updates (Phase 3)

**Live Prediction Adjustments:**

- Injury news integration
- Lineup change detection
- Market movement tracking
- Prediction recalculation triggers

### Historical Tracking (Phase 3)

**Accuracy Analysis:**

- Model performance by type
- Confidence level accuracy breakdown
- Best/worst matchup types
- Seasonal performance trends

**ROI Tracking:**

- Cumulative profit/loss
- ROI by confidence level
- Kelly Criterion effectiveness
- Bankroll growth simulation

### Monetization Features (Phase 4)

**Pick Selling Platform:**

- Free daily preview picks
- Premium subscription for all predictions
- Track record transparency
- Money-back guarantees for accuracy

**Pricing Tiers:**

- Free: 1-2 daily picks, basic predictions
- Premium: All predictions, EV analysis, model breakdowns
- Pro: Historical data, advanced analytics, betting tools

## Data Requirements

### Required NBA.com API Stats

**Base Stats:**

- PTS, FGM, FGA, FG_PCT
- FG3M, FG3A, FG3_PCT
- FTM, FTA, FT_PCT
- OREB, DREB, REB
- AST, STL, BLK, TOV, PF

**Advanced Stats:**

- OffRtg, DefRtg, NetRating
- Pace, PIE (Player Impact Estimate)
- eFG% (Effective Field Goal Percentage)

**Four Factors Stats:**

- eFG%, TOV%, OREB%, FT/FGA
- Opponent Four Factors

**Additional Data (Manual Entry MVP):**

- ELO ratings (calculate separately or use FiveThirtyEight)
- Rest days (parse schedule)
- Travel distance (manual initially)
- Injury status (manual input)
- Market odds (manual input)

## Technical Architecture

**Data Flow:**

1. Daily stats fetch from NBA.com API (stats-client)
2. Extract required fields (extract-stats)
3. Calculate ELO ratings (build ELO engine)
4. Input manual data (injuries, odds, rest)
5. Run prediction models (formulas)
6. Apply situational adjustments
7. Generate consensus and confidence
8. Calculate EV and Kelly sizing
9. Display predictions in UI
10. Cache results for performance

**File Structure:**

- `/src/lib/stats-client.ts` - NBA API fetching
- `/src/lib/extract-stats.ts` - Data extraction
- `/src/lib/formulas/moneyline/` - Prediction models
- `/src/lib/formulas/shared/` - Utilities
- `/src/app/predictions/` - Prediction UI pages
- `/src/components/predictions/` - Prediction components

## Non-Functional Requirements

**Performance:**

- Page load under 2 seconds
- Predictions generate in under 2 seconds
- API calls cached for 6 hours

**Reliability:**

- 99% uptime for prediction generation
- Graceful failure if NBA API unavailable
- Fallback to cached data

**Usability:**

- Mobile-responsive design
- Intuitive prediction display
- Clear confidence indicators
- Simple value identification

**Scalability:**

- Support all 15 daily NBA games
- Handle concurrent users (Phase 4)
- Database for historical tracking (Phase 3)

## Future Roadmap

**MVP (Phase 1) - Moneyline:**

- Build prediction engine
- Create daily prediction interface
- Manual odds and injury input
- Basic EV calculations

**Phase 2 - Spread:**

- Implement 10 spread models
- Cover probability calculations
- Spread-specific adjustments

**Phase 3 - Over/Under:**

- Implement 9 total models
- Volatility analysis
- Historical accuracy tracking
- Real-time updates

**Phase 4 - Monetization:**

- User accounts and subscriptions
- Pick selling platform
- Advanced analytics dashboard
- API for partners
