-- Using the cs3380 database
USE cs3380;

-- Arena table
CREATE TABLE Arena (
    ArenaName VARCHAR(100) PRIMARY KEY CHECK(LEN(ArenaName) > 0),
    SeatingCapacity INT CHECK(SeatingCapacity > 0),
    OpeningYear INT CHECK(OpeningYear > 1800 AND OpeningYear <= YEAR(GETDATE())),
    ArenaCityName VARCHAR(100) CHECK(LEN(ArenaCityName) > 0)
);

-- Team table
CREATE TABLE Team (
    TeamID INT PRIMARY KEY CHECK(TeamID > 0),
    TeamName VARCHAR(100) UNIQUE CHECK(LEN(TeamName) > 0),
    TeamAbbrv VARCHAR(100) UNIQUE CHECK(LEN(TeamAbbrv) > 0),
    NickName VARCHAR(100) UNIQUE CHECK(LEN(NickName) > 0),
    [State] VARCHAR(100) CHECK(LEN([State]) > 0),
    YearFounded INT CHECK(YearFounded > 1800 AND YearFounded <= YEAR(GETDATE())),
    ArenaName VARCHAR(100) REFERENCES Arena(ArenaName)
);

-- Coach table
CREATE TABLE Coach (
    CoachID INTEGER PRIMARY KEY CHECK(CoachID > 0),
    CoachName VARCHAR(100) CHECK(LEN(CoachName) > 0),
    TeamID INT REFERENCES Team(TeamID),
    SeasonsFranchise INT CHECK(SeasonsFranchise >= 0),
    SeasonsOverall INT CHECK(SeasonsOverall >= 0)
);

-- PlayOffGameCoachStats
CREATE TABLE PlayOffGameCoachStats (
    CoachID INT PRIMARY KEY REFERENCES Coach(CoachID),
    PlayoffsCurrentG INT CHECK(PlayoffsCurrentG >= 0),
    PlayoffsCurrentW INT CHECK(PlayoffsCurrentW >= 0),
    PlayoffsCurrentL INT CHECK(PlayoffsCurrentL >= 0),
    PlayoffsFranchiseG INT CHECK(PlayoffsFranchiseG >= 0),
    PlayoffsFranchiseW INT CHECK(PlayoffsFranchiseW >= 0),
    PlayoffsFranchiseL INT CHECK(PlayoffsFranchiseL >= 0),
    PlayoffsOverallG INT CHECK(PlayoffsOverallG >= 0),
    PlayoffsOverallW INT CHECK(PlayoffsOverallW >= 0),
    PlayoffsOverallL INT CHECK(PlayoffsOverallL >= 0)
);

-- RegularGameCoachStats
CREATE TABLE RegularGameCoachStats (
    CoachID INT PRIMARY KEY REFERENCES Coach(CoachID),
    RegCurrentG INT CHECK(RegCurrentG >= 0),
    RegCurrentW INT CHECK(RegCurrentW >= 0),
    RegCurrentL INT CHECK(RegCurrentL >= 0),
    RegFranchiseG INT CHECK(RegFranchiseG >= 0),
    RegFranchiseW INT CHECK(RegFranchiseW >= 0),
    RegFranchiseL INT CHECK(RegFranchiseL >= 0),
    RegOverallG INT CHECK(RegOverallG >= 0),
    RegOverallW INT CHECK(RegOverallW >= 0),
    RegOverallL INT CHECK(RegOverallL >= 0)
);

-- Player Table
CREATE TABLE Player (
    PlayerID INT PRIMARY KEY CHECK(PlayerID > 0),
    FirstName VARCHAR(100) CHECK(LEN(FirstName) > 0),
    LastName VARCHAR(100) CHECK(LEN(LastName) > 0),
    TeamID INT REFERENCES Team(TeamID)
);


-- Game 
CREATE TABLE Game (
    GameID INT PRIMARY KEY CHECK(GameID > 0),
    [Date] DATE CHECK(YEAR([Date]) >= 2024),
    HomePTS INT CHECK(HomePTS >= 0),
    VisitorPTS INT CHECK(VisitorPTS >= 0),
    [Length] TIME,
    Arena VARCHAR(100) REFERENCES Arena(ArenaName),
    Overtime CHAR(2) CHECK(Overtime IN ('N','Y','2Y','3Y', '4Y')),
    AttendingAmount INTEGER CHECK(AttendingAmount >= 0),
    HomeTeamID INT REFERENCES Team(TeamID),
    VisitorTeamID INT REFERENCES Team(TeamID),
    CHECK(HomeTeamID != VisitorTeamID)
);

-- PlayInGame table
CREATE TABLE PlayInGame (
    PlayerID INT NOT NULL REFERENCES Player(PlayerID),
    GameID INT NOT NULL REFERENCES Game(GameID),
    TeamID INT REFERENCES Team(TeamID),
    MP NUMERIC(5,2) CHECK(MP >= 0),
    FG INT CHECK(FG >= 0),
    FGA INT CHECK(FGA >= 0),
    [3P] INT CHECK([3P] >= 0),
    [3PA] INT CHECK([3PA] >= 0),
    FT INT CHECK(FT >= 0),
    FTA INT CHECK(FTA >= 0),
    AST INT CHECK(AST >= 0),
    STL INT CHECK(STL >= 0),
    PRIMARY KEY (PlayerID, GameID)
);

-- PlayerInformation table
CREATE TABLE PlayerInformation (
    PlayerID INT PRIMARY KEY REFERENCES Player(PlayerID),
    Birthdate DATE,
    School VARCHAR(100) CHECK(LEN(School) > 0),
    Country VARCHAR(100) CHECK(LEN(Country) > 0),
    [Weight] INT CHECK([Weight] > 0),
    SeasonsPlayed INT CHECK(SeasonsPlayed >= 0),
    Position VARCHAR(100) CHECK(LEN(Position) > 0),
    FromYear INT CHECK(FromYear > 0),
    ToYear INT CHECK(ToYear > 0),
    Height VARCHAR(10),
    IsActive INT CHECK(IsActive = 0 OR IsActive = 1),
    CHECK(ToYear >= FromYear)
);

-- DraftCombine table
CREATE TABLE DraftCombine (
    Season INT NOT NULL CHECK(Season >= 1900),
    PlayerID INT NOT NULL REFERENCES Player(PlayerID),
    Wingspan NUMERIC(5,2) CHECK(Wingspan > 0),
    StandingReach NUMERIC(5,2) CHECK(StandingReach > 0),
    BodyFatPct NUMERIC(4,2) CHECK(BodyFatPct > 0),
    StandingVerticalLeap NUMERIC(4,2) CHECK(StandingVerticalLeap > 0),
    MaximumVerticalLeap Numeric(3,1) CHECK(MaximumVerticalLeap > 0),
    LaneAgilityTime NUMERIC(4,2) CHECK(LaneAgilityTime > 0),
    ThreeQuarterSprint NUMERIC(4,2) CHECK(ThreeQuarterSprint > 0),
    BenchPress INT CHECK(BenchPress >= 0),
    PRIMARY KEY (Season, PlayerID)
);


-- Organization table
CREATE TABLE Organization (
    OrganizationID INT PRIMARY KEY CHECK(OrganizationID > 0),
    OrganizationName VARCHAR(100) CHECK(LEN(OrganizationName) > 0),
    OrganizationType VARCHAR(100) CHECK(LEN(OrganizationType) > 0)
);

-- Draft table
CREATE TABLE Drafts (
    DraftID INT PRIMARY KEY CHECK(DraftID > 0),
    PlayerID INT REFERENCES Player(PlayerID),
    TeamID INT REFERENCES Team(TeamID),
    OrganizationID INT REFERENCES Organization(OrganizationID),
    Season INT CHECK(Season >= 1900),
    RoundNumber INT CHECK(RoundNumber >= 0),
    RoundPick INT CHECK(RoundPick >= 0),
    OverallPick INT CHECK(OverallPick >= 0),
    DraftType VARCHAR(20) CHECK (DraftType IN ('Draft' , 'Territorial'))
);

