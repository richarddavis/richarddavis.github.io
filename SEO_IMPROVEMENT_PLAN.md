# SEO Improvement Plan for Richard Lee Davis

## Executive Summary

Your Jekyll-based academic website has excellent potential for search engine optimization. The foundation is solid with proper sitemap generation and structure, but several key optimizations are needed to improve your visibility for searches like "Richard Lee Davis", "learning sciences KTH", "educational technology Sweden", and "AI in education Europe".

## 🚀 Immediate Actions (High Impact, Low Effort)

### 1. Enable Open Graph and Schema.org Metadata
**Current Issue**: Your `_config.yml` has `serve_og_meta: false` and `serve_schema_org: false`

**Fix**: Update these settings in `_config.yml`:
```yaml
serve_og_meta: true
serve_schema_org: true
```

**Impact**: This will dramatically improve how your site appears when shared on social media and helps search engines understand your content structure.

### 2. Add Google Search Console Verification
**Current Issue**: No Google Search Console verification configured

**Fix**: 
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add your site: `https://richarddavis.github.io`
3. Get your verification code
4. Add it to `_config.yml`:
```yaml
google_site_verification: YOUR_VERIFICATION_CODE_HERE
```

**Impact**: Essential for Google indexing and monitoring your site's search performance.

### 3. Set Up Google Analytics
**Current Issue**: No analytics tracking configured

**Fix**: Add Google Analytics to track SEO performance:
```yaml
google_analytics: G-XXXXXXXXXX  # Your GA4 measurement ID
```

### 4. Optimize Your Site Description
**Current Issue**: Generic description in `_config.yml`

**Fix**: Replace the current description with SEO-optimized text:
```yaml
description: >
  Dr. Richard Lee Davis - Assistant Professor of Learning Sciences and Educational Technology at KTH Royal Institute of Technology, Stockholm, Sweden. Research in AI/ML in education, human-computer interaction, and STEM education. Expert in constructionist learning, digital fabrication, and educational technology design.
```

### 5. Update Keywords for Better Targeting
**Current Issue**: Current keywords are too generic

**Fix**: Replace with targeted keywords:
```yaml
keywords: richard-lee-davis, learning-sciences, educational-technology, AI-in-education, KTH-royal-institute-technology, stockholm-sweden, human-computer-interaction, STEM-education, constructionist-learning, digital-fabrication, learning-analytics, educational-AI, europe-education-research
```

## 📈 Content Optimization (Medium Impact, Medium Effort)

### 6. Enhance Your About Page
**Current Issue**: The about page lacks structured SEO optimization

**Fix**: Add structured data and optimize content:
- Add location-specific content about KTH, Stockholm, and Sweden
- Include your research keywords naturally in the text
- Add a section about your work in European educational technology

### 7. Create Location-Specific Content
**Why**: You want to rank for "Sweden", "KTH", and "Europe" searches

**Actions**:
- Add a dedicated page about your work at KTH
- Create content about educational technology research in Sweden/Europe
- Include mentions of Stockholm, Sweden, and European educational initiatives

### 8. Add Structured Data for Academic Profile
**Fix**: The theme already supports this through schema.org, but ensure your academic credentials are properly structured:
- Add your ORCID ID to `_config.yml`
- Include your Google Scholar profile
- Add your institutional affiliation details

## 🔧 Technical SEO (High Impact, Medium Effort)

### 9. Create a Custom Domain (Recommended)
**Current Issue**: Using `richarddavis.github.io` subdomain

**Benefits**: 
- Better brand recognition
- Improved search rankings
- More professional appearance

**Suggestion**: Consider purchasing `richardleedavis.com` or `richarddavis.se` (Sweden domain)

### 10. Optimize Page Titles and Meta Descriptions
**Current Issue**: Page titles aren't optimized for search

**Fix**: Update page frontmatter to include SEO-optimized titles:
```yaml
---
title: "Richard Lee Davis - Learning Sciences & Educational Technology Researcher"
description: "Dr. Richard Lee Davis, Assistant Professor at KTH Royal Institute of Technology. Research in AI/ML in education, human-computer interaction, and STEM education in Sweden and Europe."
---
```

### 11. Create a Sitemap Page
**Current Issue**: While you have XML sitemap, no HTML sitemap for users

**Fix**: Create an HTML sitemap page to help users and search engines navigate your site.

## 🌍 Local SEO for Sweden/KTH (Medium Impact, Low Effort)

### 12. Optimize for Local Search
**Add location-specific content**:
- "Educational Technology Research in Sweden"
- "KTH Royal Institute of Technology Faculty"
- "Stockholm Learning Sciences"
- "European AI in Education Research"

### 13. Create Location Pages
**Create dedicated pages for**:
- Your work at KTH
- Research collaborations in Sweden
- European educational technology initiatives

## 📊 Monitoring and Measurement

### 14. Set Up Search Console Monitoring
**Track these search queries**:
- "Richard Lee Davis"
- "learning sciences KTH"
- "educational technology Sweden"
- "AI in education Europe"

### 15. Monitor Your Progress
**Monthly checks**:
- Google Search Console performance
- Search rankings for target keywords
- Site indexing status
- Click-through rates

## 📝 Content Strategy for Long-term SEO

### 16. Blog Content Strategy
**Create regular content about**:
- Your research findings
- Educational technology trends in Europe
- AI in education developments
- Learning sciences innovations at KTH

### 17. Publication Integration
**Optimize your publications page**:
- Add abstracts with keywords
- Include conference locations (Europe, Sweden)
- Add research area tags

## 🎯 Target Keyword Strategy

### Primary Keywords (High Priority)
1. "Richard Lee Davis" - Personal branding
2. "learning sciences KTH" - Institution + field
3. "educational technology Sweden" - Location + field
4. "AI in education Europe" - Technology + location

### Secondary Keywords (Medium Priority)
1. "constructionist learning research"
2. "digital fabrication education"
3. "learning analytics Sweden"
4. "educational AI KTH"
5. "STEM education technology"

### Long-tail Keywords (Low Priority)
1. "Richard Lee Davis KTH Royal Institute Technology"
2. "learning sciences research Stockholm Sweden"
3. "educational technology professor KTH"
4. "AI machine learning education Europe"

## 📋 Implementation Checklist

### Week 1 (Immediate Impact)
- [ ] Enable Open Graph and Schema.org metadata
- [ ] Set up Google Search Console
- [ ] Update site description and keywords
- [ ] Set up Google Analytics

### Week 2 (Content Optimization)
- [ ] Optimize about page content
- [ ] Add location-specific content
- [ ] Update page titles and descriptions

### Week 3 (Technical Improvements)
- [ ] Create HTML sitemap
- [ ] Optimize images with alt text
- [ ] Add structured data for academic profile

### Week 4 (Monitoring Setup)
- [ ] Set up tracking for target keywords
- [ ] Create content calendar for regular updates
- [ ] Monitor initial performance metrics

## 🚀 Quick Wins for Immediate Implementation

1. **Change these two lines in `_config.yml`**:
   ```yaml
   serve_og_meta: true
   serve_schema_org: true
   ```

2. **Add Google Search Console verification**

3. **Update your site description with location and field keywords**

4. **Create one blog post titled**: "Educational Technology Research at KTH Royal Institute of Technology"

## Expected Results

**Timeline**: 
- **1-2 weeks**: Improved indexing and social sharing
- **4-6 weeks**: Better rankings for "Richard Lee Davis"
- **2-3 months**: Improved rankings for location-specific searches
- **6+ months**: Established authority for your research areas

**Target Rankings**:
- "Richard Lee Davis": Top 3 results
- "learning sciences KTH": Top 5 results
- "educational technology Sweden": Top 10 results
- "AI in education Europe": Top 15 results

Start with the immediate actions listed above - they'll provide the biggest impact with minimal effort. The technical foundation of your site is already solid, so these optimizations should yield relatively quick results.