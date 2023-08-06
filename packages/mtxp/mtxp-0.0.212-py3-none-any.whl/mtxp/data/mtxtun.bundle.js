#!/usr/bin/env node
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ([
/* 0 */,
/* 1 */
/***/ ((module) => {

module.exports = require("@nestjs/core");

/***/ }),
/* 2 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AppModule = void 0;
const common_1 = __webpack_require__(3);
const config_1 = __webpack_require__(4);
const app_controller_1 = __webpack_require__(5);
const app_service_1 = __webpack_require__(17);
const auth_module_1 = __webpack_require__(18);
const users_module_1 = __webpack_require__(19);
const schedule_1 = __webpack_require__(29);
const config_2 = __importDefault(__webpack_require__(30));
const nestjs_prisma_1 = __webpack_require__(9);
const logger_service_1 = __webpack_require__(16);
const bot_module_1 = __webpack_require__(31);
let AppModule = class AppModule {
};
AppModule = __decorate([
    (0, common_1.Module)({
        imports: [
            config_1.ConfigModule.forRoot({ isGlobal: true, load: [config_2.default] }),
            schedule_1.ScheduleModule.forRoot(),
            nestjs_prisma_1.PrismaModule.forRootAsync({
                isGlobal: true,
                useFactory: async (configService) => {
                    return {
                        prismaOptions: {
                            log: ['info', 'query'],
                            datasources: {
                                db: {
                                    url: configService.get('DATABASE_URL'),
                                },
                            },
                        },
                        explicitConnect: configService.get('explicit'),
                    };
                },
                inject: [config_1.ConfigService],
            }),
            auth_module_1.AuthModule,
            users_module_1.UsersModule,
            bot_module_1.BotModule,
        ],
        controllers: [app_controller_1.AppController],
        providers: [logger_service_1.DefaultLoggerService, app_service_1.AppService],
    })
], AppModule);
exports.AppModule = AppModule;


/***/ }),
/* 3 */
/***/ ((module) => {

module.exports = require("@nestjs/common");

/***/ }),
/* 4 */
/***/ ((module) => {

module.exports = require("@nestjs/config");

/***/ }),
/* 5 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var _a, _b, _c;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AppController = void 0;
const common_1 = __webpack_require__(3);
const express_1 = __webpack_require__(6);
const auth_service_1 = __webpack_require__(7);
const jwt_auth_guard_1 = __webpack_require__(13);
const local_auth_guard_1 = __webpack_require__(15);
const logger_service_1 = __webpack_require__(16);
let AppController = class AppController {
    constructor(authService, logger) {
        this.authService = authService;
        this.logger = logger;
    }
    async home() {
        return 'mtxtunv2 default home';
    }
    async login(req, res) {
        this.logger.log(`用户登录 ${req.user.email}`);
        const token = this.authService.generateTokens({
            userId: req.user.id,
            roles: req.user.roles2.map((r) => r.name),
        });
        const auth_token = token.accessToken;
        res.set({ 'x-access-token': auth_token }).json({
            type: "account",
            userinfo: req.user,
            token: token,
        });
    }
    async me(req) {
        this.logger.log(`TODO: 通过数据库获取真正的用户信息`);
        return {
            success: true,
            data: {
                name: 'Serati Ma22',
                avatar: 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
                userid: '00000001',
                email: 'antdesign@alipay.com',
                signature: '海纳百川，有容乃大',
                title: '交互专家',
                group: '蚂蚁金服－某某某事业群－某某平台部－某某技术部－UED',
                tags: [
                    {
                        key: '0',
                        label: '很有想法的',
                    },
                    {
                        key: '1',
                        label: '专注设计',
                    },
                    {
                        key: '2',
                        label: '辣~',
                    },
                    {
                        key: '3',
                        label: '大长腿',
                    },
                    {
                        key: '4',
                        label: '川妹子',
                    },
                    {
                        key: '5',
                        label: '海纳百川',
                    },
                ],
                notifyCount: 12,
                unreadCount: 11,
                country: 'China',
                geographic: {
                    province: {
                        label: '浙江省',
                        key: '330000',
                    },
                    city: {
                        label: '杭州市',
                        key: '330100',
                    },
                },
                address: '西湖区工专路 77 号',
                phone: '0752-268888888',
            },
        };
    }
    getProfile(req) {
        return req.user;
    }
};
__decorate([
    (0, common_1.Get)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], AppController.prototype, "home", null);
__decorate([
    (0, common_1.UseGuards)(local_auth_guard_1.LocalAuthGuard),
    (0, common_1.Post)('auth/login'),
    __param(0, (0, common_1.Request)()),
    __param(1, (0, common_1.Response)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, typeof (_a = typeof express_1.Response !== "undefined" && express_1.Response) === "function" ? _a : Object]),
    __metadata("design:returntype", Promise)
], AppController.prototype, "login", null);
__decorate([
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    (0, common_1.Get)('auth/me'),
    __param(0, (0, common_1.Request)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object]),
    __metadata("design:returntype", Promise)
], AppController.prototype, "me", null);
__decorate([
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard),
    (0, common_1.Get)('profile'),
    __param(0, (0, common_1.Request)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object]),
    __metadata("design:returntype", void 0)
], AppController.prototype, "getProfile", null);
AppController = __decorate([
    (0, common_1.Controller)(),
    __metadata("design:paramtypes", [typeof (_b = typeof auth_service_1.AuthService !== "undefined" && auth_service_1.AuthService) === "function" ? _b : Object, typeof (_c = typeof logger_service_1.DefaultLoggerService !== "undefined" && logger_service_1.DefaultLoggerService) === "function" ? _c : Object])
], AppController);
exports.AppController = AppController;


/***/ }),
/* 6 */
/***/ ((module) => {

module.exports = require("express");

/***/ }),
/* 7 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var _a, _b, _c, _d, _e;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AuthService = void 0;
const common_1 = __webpack_require__(3);
const users_service_1 = __webpack_require__(8);
const jwt_1 = __webpack_require__(10);
const nestjs_prisma_1 = __webpack_require__(9);
const password_service_1 = __webpack_require__(11);
const config_1 = __webpack_require__(4);
let AuthService = class AuthService {
    constructor(usersService, jwtService, prisma, passwordService, configService) {
        this.usersService = usersService;
        this.jwtService = jwtService;
        this.prisma = prisma;
        this.passwordService = passwordService;
        this.configService = configService;
    }
    async validateUser(username, passwd) {
        const user = await this.usersService.findOne(username);
        const passwordValid = await this.passwordService.validatePassword(passwd, user.password);
        if (!passwordValid) {
            return null;
        }
        const { password } = user, result = __rest(user, ["password"]);
        return result;
    }
    refreshToken(token) {
        try {
            const { userId, roles } = this.jwtService.verify(token, {
                secret: this.configService.get('JWT_REFRESH_SECRET'),
            });
            return this.generateTokens({
                userId,
                roles,
            });
        }
        catch (e) {
            throw new common_1.UnauthorizedException();
        }
    }
    generateTokens(payload) {
        return {
            accessToken: this.generateAccessToken(payload),
            refreshToken: this.generateRefreshToken(payload),
        };
    }
    generateAccessToken(payload) {
        return this.jwtService.sign(payload);
    }
    generateRefreshToken(payload) {
        const securityConfig = this.configService.get('security');
        return this.jwtService.sign(payload, {
            secret: this.configService.get('JWT_REFRESH_SECRET'),
            expiresIn: securityConfig.refreshIn,
        });
    }
    async login(email, password) {
        const user = await this.prisma.user.findUnique({
            where: { email },
            include: { roles: true },
        });
        if (!user) {
            return null;
        }
        const passwordValid = await this.passwordService.validatePassword(password, user.password);
        if (!passwordValid) {
            return null;
        }
        return this.generateTokens({
            userId: user.id,
            roles: user.roles.map((r) => r.name),
        });
    }
    async changePassword(userId, userPassword, changePassword) {
        const passwordValid = await this.passwordService.validatePassword(changePassword.oldPassword, userPassword);
        if (!passwordValid) {
            throw new common_1.BadRequestException('Invalid password');
        }
        const hashedPassword = await this.passwordService.hashPassword(changePassword.newPassword);
        return this.prisma.user.update({
            data: {
                password: hashedPassword,
            },
            where: { id: userId },
        });
    }
};
AuthService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof users_service_1.UsersService !== "undefined" && users_service_1.UsersService) === "function" ? _a : Object, typeof (_b = typeof jwt_1.JwtService !== "undefined" && jwt_1.JwtService) === "function" ? _b : Object, typeof (_c = typeof nestjs_prisma_1.PrismaService !== "undefined" && nestjs_prisma_1.PrismaService) === "function" ? _c : Object, typeof (_d = typeof password_service_1.PasswordService !== "undefined" && password_service_1.PasswordService) === "function" ? _d : Object, typeof (_e = typeof config_1.ConfigService !== "undefined" && config_1.ConfigService) === "function" ? _e : Object])
], AuthService);
exports.AuthService = AuthService;


/***/ }),
/* 8 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.UsersService = void 0;
const common_1 = __webpack_require__(3);
const nestjs_prisma_1 = __webpack_require__(9);
let UsersService = class UsersService {
    constructor(prisma) {
        this.prisma = prisma;
    }
    async findOne(username) {
        return this.prisma.user.findUnique({
            where: { email: username },
        });
    }
    async getUserById(userId) {
        return this.prisma.user.findUnique({
            where: { id: userId },
            include: { roles: true },
        });
    }
    async queryUsers(currPage = 0, pageSize = 20) {
        const data = await this.prisma.user.findMany();
        return {
            data: data,
            current: 1,
            pageSize: 20,
            success: true,
            total: await this.prisma.user.count()
        };
    }
};
UsersService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof nestjs_prisma_1.PrismaService !== "undefined" && nestjs_prisma_1.PrismaService) === "function" ? _a : Object])
], UsersService);
exports.UsersService = UsersService;


/***/ }),
/* 9 */
/***/ ((module) => {

module.exports = require("nestjs-prisma");

/***/ }),
/* 10 */
/***/ ((module) => {

module.exports = require("@nestjs/jwt");

/***/ }),
/* 11 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PasswordService = void 0;
const common_1 = __webpack_require__(3);
const config_1 = __webpack_require__(4);
const bcryptjs_1 = __webpack_require__(12);
let PasswordService = class PasswordService {
    constructor(configService) {
        this.configService = configService;
    }
    get bcryptSaltRounds() {
        const securityConfig = this.configService.get('security');
        const saltOrRounds = securityConfig.bcryptSaltOrRound;
        return Number.isInteger(Number(saltOrRounds))
            ? Number(saltOrRounds)
            : saltOrRounds;
    }
    validatePassword(password, hashedPassword) {
        return (0, bcryptjs_1.compare)(password, hashedPassword);
    }
    hashPassword(password) {
        return (0, bcryptjs_1.hash)(password, this.bcryptSaltRounds);
    }
};
PasswordService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof config_1.ConfigService !== "undefined" && config_1.ConfigService) === "function" ? _a : Object])
], PasswordService);
exports.PasswordService = PasswordService;


/***/ }),
/* 12 */
/***/ ((module) => {

module.exports = require("bcryptjs");

/***/ }),
/* 13 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.JwtAuthGuard = void 0;
const common_1 = __webpack_require__(3);
const passport_1 = __webpack_require__(14);
let JwtAuthGuard = class JwtAuthGuard extends (0, passport_1.AuthGuard)('jwt') {
};
JwtAuthGuard = __decorate([
    (0, common_1.Injectable)()
], JwtAuthGuard);
exports.JwtAuthGuard = JwtAuthGuard;


/***/ }),
/* 14 */
/***/ ((module) => {

module.exports = require("@nestjs/passport");

/***/ }),
/* 15 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LocalAuthGuard = void 0;
const common_1 = __webpack_require__(3);
const passport_1 = __webpack_require__(14);
let LocalAuthGuard = class LocalAuthGuard extends (0, passport_1.AuthGuard)('local') {
};
LocalAuthGuard = __decorate([
    (0, common_1.Injectable)()
], LocalAuthGuard);
exports.LocalAuthGuard = LocalAuthGuard;


/***/ }),
/* 16 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DefaultLoggerService = exports.MyLogger = void 0;
const common_1 = __webpack_require__(3);
class MyLogger {
    log(message, ...optionalParams) {
        console.log("log:", message);
    }
    error(message, ...optionalParams) {
        console.log("error:", message);
    }
    warn(message, ...optionalParams) {
        console.log("warn:", message);
    }
    debug(message, ...optionalParams) {
        console.log("debug:", message);
    }
    verbose(message, ...optionalParams) {
        console.log("verbose:", message);
    }
}
exports.MyLogger = MyLogger;
class DefaultLoggerService extends common_1.ConsoleLogger {
    error(message, stack, context) {
        super.error(message, stack, context);
    }
}
exports.DefaultLoggerService = DefaultLoggerService;


/***/ }),
/* 17 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AppService = void 0;
const common_1 = __webpack_require__(3);
let AppService = class AppService {
    getHello() {
        return 'Hello World!';
    }
};
AppService = __decorate([
    (0, common_1.Injectable)()
], AppService);
exports.AppService = AppService;


/***/ }),
/* 18 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.AuthModule = void 0;
const common_1 = __webpack_require__(3);
const config_1 = __webpack_require__(4);
const jwt_1 = __webpack_require__(10);
const passport_1 = __webpack_require__(14);
const nestjs_prisma_1 = __webpack_require__(9);
const users_module_1 = __webpack_require__(19);
const auth_service_1 = __webpack_require__(7);
const password_service_1 = __webpack_require__(11);
const jwt_strategy_1 = __webpack_require__(25);
const local_strategy_1 = __webpack_require__(27);
let AuthModule = class AuthModule {
};
AuthModule = __decorate([
    (0, common_1.Module)({
        imports: [
            passport_1.PassportModule.register({ defaultStrategy: 'jwt' }),
            jwt_1.JwtModule.registerAsync({
                useFactory: async (configService) => {
                    const securityConfig = configService.get('security');
                    return {
                        secret: configService.get('JWT_ACCESS_SECRET'),
                        signOptions: {
                            expiresIn: securityConfig.expiresIn,
                        },
                    };
                },
                inject: [config_1.ConfigService],
            }),
            users_module_1.UsersModule,
            passport_1.PassportModule,
        ],
        providers: [
            nestjs_prisma_1.PrismaService,
            users_module_1.UsersModule,
            auth_service_1.AuthService,
            local_strategy_1.LocalStrategy,
            jwt_strategy_1.JwtStrategy,
            password_service_1.PasswordService,
        ],
        exports: [auth_service_1.AuthService],
    })
], AuthModule);
exports.AuthModule = AuthModule;


/***/ }),
/* 19 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.UsersModule = void 0;
const common_1 = __webpack_require__(3);
const nestjs_prisma_1 = __webpack_require__(9);
const logger_service_1 = __webpack_require__(16);
const user_controller_1 = __webpack_require__(20);
const users_service_1 = __webpack_require__(8);
let UsersModule = class UsersModule {
};
UsersModule = __decorate([
    (0, common_1.Module)({
        providers: [nestjs_prisma_1.PrismaService, users_service_1.UsersService, logger_service_1.DefaultLoggerService],
        controllers: [user_controller_1.UserController],
        exports: [users_service_1.UsersService],
    })
], UsersModule);
exports.UsersModule = UsersModule;


/***/ }),
/* 20 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a, _b;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.UserController = void 0;
const common_1 = __webpack_require__(3);
const jwt_auth_guard_1 = __webpack_require__(13);
const roles_guard_1 = __webpack_require__(21);
const constants_1 = __webpack_require__(23);
const roles_decorator_1 = __webpack_require__(24);
const logger_service_1 = __webpack_require__(16);
const users_service_1 = __webpack_require__(8);
let UserController = class UserController {
    constructor(logger, usersService) {
        this.logger = logger;
        this.usersService = usersService;
    }
    async list() {
        const result = await this.usersService.queryUsers();
        return result;
    }
};
__decorate([
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard, roles_guard_1.RolesGuard),
    (0, roles_decorator_1.Roles)(constants_1.ROLE_ADMIN),
    (0, common_1.Get)(),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], UserController.prototype, "list", null);
UserController = __decorate([
    (0, common_1.Controller)("user"),
    __metadata("design:paramtypes", [typeof (_a = typeof logger_service_1.DefaultLoggerService !== "undefined" && logger_service_1.DefaultLoggerService) === "function" ? _a : Object, typeof (_b = typeof users_service_1.UsersService !== "undefined" && users_service_1.UsersService) === "function" ? _b : Object])
], UserController);
exports.UserController = UserController;


/***/ }),
/* 21 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RolesGuard = void 0;
const common_1 = __webpack_require__(3);
const core_1 = __webpack_require__(1);
const graphql_1 = __webpack_require__(22);
let RolesGuard = class RolesGuard {
    constructor(reflector) {
        this.reflector = reflector;
    }
    canActivate(context) {
        const ctx = graphql_1.GqlExecutionContext.create(context);
        const request = ctx.getContext().req;
        const user = request.user;
        const requireRole = this.reflector.getAllAndOverride('roles', [context.getHandler(), context.getClass()]);
        if (!requireRole)
            return true;
        if (!user) {
            return false;
        }
        return requireRole.some((role) => {
            var _a;
            return (_a = user === null || user === void 0 ? void 0 : user.roles) === null || _a === void 0 ? void 0 : _a.find(roleObj => {
                return roleObj.name === role;
            });
        });
    }
};
RolesGuard = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof core_1.Reflector !== "undefined" && core_1.Reflector) === "function" ? _a : Object])
], RolesGuard);
exports.RolesGuard = RolesGuard;


/***/ }),
/* 22 */
/***/ ((module) => {

module.exports = require("@nestjs/graphql");

/***/ }),
/* 23 */
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SUB_TASK_REPOSITORY = exports.TODO_ITEM_REPOSITORY = exports.DEMO_REPOSITORY = exports.POST_REPOSITORY = exports.USER_REPOSITORY = exports.PRODUCTION = exports.TEST = exports.DEVELOPMENT = exports.SEQUELIZE = exports.CONFIG_AWS_REGION = exports.CONFIG_AWS_SECRET_ACCESS_KEY = exports.CONFIG_AWS_ACCESS_KEY_ID = exports.CONFIG_MEDIA_BUCKET = exports.AUTH_HEADER_NAME = exports.ROLE_ADMIN = void 0;
exports.ROLE_ADMIN = "Admin";
exports.AUTH_HEADER_NAME = 'authorization';
exports.CONFIG_MEDIA_BUCKET = "MEDIA_BUCKET";
exports.CONFIG_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID";
exports.CONFIG_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY";
exports.CONFIG_AWS_REGION = "AWS_REGION";
exports.SEQUELIZE = 'SEQUELIZE';
exports.DEVELOPMENT = 'development';
exports.TEST = 'test';
exports.PRODUCTION = 'production';
exports.USER_REPOSITORY = 'USER_REPOSITORY';
exports.POST_REPOSITORY = 'POST_REPOSITORY';
exports.DEMO_REPOSITORY = 'DEMO_REPOSITORY';
exports.TODO_ITEM_REPOSITORY = 'TODO_ITEM_REPOSITORY';
exports.SUB_TASK_REPOSITORY = 'SUB_TASK_REPOSITORY';


/***/ }),
/* 24 */
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Roles = void 0;
const common_1 = __webpack_require__(3);
const Roles = (...roles) => (0, common_1.SetMetadata)('roles', roles);
exports.Roles = Roles;


/***/ }),
/* 25 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a, _b, _c;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.JwtStrategy = void 0;
const passport_jwt_1 = __webpack_require__(26);
const passport_1 = __webpack_require__(14);
const common_1 = __webpack_require__(3);
const config_1 = __webpack_require__(4);
const auth_service_1 = __webpack_require__(7);
const users_service_1 = __webpack_require__(8);
let JwtStrategy = class JwtStrategy extends (0, passport_1.PassportStrategy)(passport_jwt_1.Strategy) {
    constructor(authService, userService, configService) {
        super({
            jwtFromRequest: passport_jwt_1.ExtractJwt.fromAuthHeaderAsBearerToken(),
            secretOrKey: configService.get('JWT_ACCESS_SECRET'),
        });
        this.authService = authService;
        this.userService = userService;
        this.configService = configService;
    }
    async validate(payload) {
        const user = await this.userService.getUserById(payload.userId);
        return user;
    }
};
JwtStrategy = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof auth_service_1.AuthService !== "undefined" && auth_service_1.AuthService) === "function" ? _a : Object, typeof (_b = typeof users_service_1.UsersService !== "undefined" && users_service_1.UsersService) === "function" ? _b : Object, typeof (_c = typeof config_1.ConfigService !== "undefined" && config_1.ConfigService) === "function" ? _c : Object])
], JwtStrategy);
exports.JwtStrategy = JwtStrategy;


/***/ }),
/* 26 */
/***/ ((module) => {

module.exports = require("passport-jwt");

/***/ }),
/* 27 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var _a;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LocalStrategy = void 0;
const common_1 = __webpack_require__(3);
const passport_1 = __webpack_require__(14);
const passport_local_1 = __webpack_require__(28);
const auth_service_1 = __webpack_require__(7);
let LocalStrategy = class LocalStrategy extends (0, passport_1.PassportStrategy)(passport_local_1.Strategy) {
    constructor(authService) {
        super();
        this.authService = authService;
    }
    async validate(username, password) {
        const user = await this.authService.validateUser(username, password);
        if (!user) {
            throw new common_1.UnauthorizedException();
        }
        return user;
    }
};
LocalStrategy = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof auth_service_1.AuthService !== "undefined" && auth_service_1.AuthService) === "function" ? _a : Object])
], LocalStrategy);
exports.LocalStrategy = LocalStrategy;


/***/ }),
/* 28 */
/***/ ((module) => {

module.exports = require("passport-local");

/***/ }),
/* 29 */
/***/ ((module) => {

module.exports = require("@nestjs/schedule");

/***/ }),
/* 30 */
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
const config = {
    PORT: process.env.PORT || '3210',
    JWT_ACCESS_SECRET: 'SGv9nGjks9as;df9)AKdfhsS@#ydHk(FF$lnM<)gf8s*mDDUJAShp-0sd',
    JWT_REFRESH_SECRET: 'msUJASf8d*)df<)gdsS8JJSDfDnp-0sdjyhHk@#MFFDnn8K8jhks2$l(9',
    SMIRROR_CC: 'http://www.baidu.com',
    TOR_HEDDEN_KEY: 'v3key----',
    static_dir: "public",
    cors: {
        enabled: true,
    },
    graphql: {
        playgroundEnabled: true,
        debug: true,
        schemaDestination: './src/schema.graphql',
        sortSchema: true,
    },
    security: {
        expiresIn: '360m',
        refreshIn: '7d',
        bcryptSaltOrRound: 10,
    },
    aws: {
        region: 'us-east-1',
        bucket: 'mtxcms-default-1-storage',
        secretAccessKey: null,
        accessKeyId: null,
    },
    db: {
        dbHost: process.env.MTX_DB_HOST || '127.0.0.1',
        dbPort: process.env.MTX_DB_PORT || '5432',
        dbUser: process.env.MTX_DB_USER || 'postgres',
        dbPassword: process.env.MTX_DB_PASSWORD || '',
        dbName: process.env.MTX_DB_NAME || 'test',
        dbSchema: process.env.MTX_DB_SCHEMA || 'public',
        dbType: process.env.MTX_DB_TYPE || 'postgres',
    },
    max_page_size: 1000,
};
exports["default"] = () => {
    return config;
};


/***/ }),
/* 31 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.BotModule = void 0;
const common_1 = __webpack_require__(3);
const nestjs_prisma_1 = __webpack_require__(9);
const logger_service_1 = __webpack_require__(16);
const bot_controller_1 = __webpack_require__(32);
const bot_service_1 = __webpack_require__(33);
let BotModule = class BotModule {
};
BotModule = __decorate([
    (0, common_1.Module)({
        providers: [nestjs_prisma_1.PrismaService, bot_service_1.BotService, logger_service_1.DefaultLoggerService],
        controllers: [bot_controller_1.BotController],
        exports: [bot_service_1.BotService],
    })
], BotModule);
exports.BotModule = BotModule;


/***/ }),
/* 32 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
var _a, _b, _c, _d;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.BotController = void 0;
const common_1 = __webpack_require__(3);
const jwt_auth_guard_1 = __webpack_require__(13);
const roles_guard_1 = __webpack_require__(21);
const constants_1 = __webpack_require__(23);
const roles_decorator_1 = __webpack_require__(24);
const logger_service_1 = __webpack_require__(16);
const bot_service_1 = __webpack_require__(33);
const createBot_dto_1 = __webpack_require__(35);
const findAllBot_dto_1 = __webpack_require__(37);
let BotController = class BotController {
    constructor(botService, logger) {
        this.botService = botService;
        this.logger = logger;
    }
    async findAll(findAllBotDto) {
        const result = await this.botService.findAll(findAllBotDto);
        return result;
    }
    async Create(body) {
        const result = await this.botService.create(body);
        return result;
    }
};
__decorate([
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard, roles_guard_1.RolesGuard),
    (0, roles_decorator_1.Roles)(constants_1.ROLE_ADMIN),
    (0, common_1.Get)(),
    __param(0, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [typeof (_a = typeof findAllBot_dto_1.FindAllBotDto !== "undefined" && findAllBot_dto_1.FindAllBotDto) === "function" ? _a : Object]),
    __metadata("design:returntype", Promise)
], BotController.prototype, "findAll", null);
__decorate([
    (0, common_1.UseGuards)(jwt_auth_guard_1.JwtAuthGuard, roles_guard_1.RolesGuard),
    (0, roles_decorator_1.Roles)(constants_1.ROLE_ADMIN),
    (0, common_1.Post)(),
    __param(0, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [typeof (_b = typeof createBot_dto_1.CreateBotDto !== "undefined" && createBot_dto_1.CreateBotDto) === "function" ? _b : Object]),
    __metadata("design:returntype", Promise)
], BotController.prototype, "Create", null);
BotController = __decorate([
    (0, common_1.Controller)("bot"),
    __metadata("design:paramtypes", [typeof (_c = typeof bot_service_1.BotService !== "undefined" && bot_service_1.BotService) === "function" ? _c : Object, typeof (_d = typeof logger_service_1.DefaultLoggerService !== "undefined" && logger_service_1.DefaultLoggerService) === "function" ? _d : Object])
], BotController);
exports.BotController = BotController;


/***/ }),
/* 33 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var _a;
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.BotService = void 0;
const common_1 = __webpack_require__(3);
const nestjs_prisma_1 = __webpack_require__(9);
const lodash_1 = __importDefault(__webpack_require__(34));
let BotService = class BotService {
    constructor(prisma) {
        this.prisma = prisma;
    }
    async create(data) {
        return this.prisma.bot.create({
            data: data
        });
    }
    async findAll(findAllBotDto) {
        const entity_name = "bot";
        const page_size = lodash_1.default.min([findAllBotDto.pageSize, 1000]);
        const baseWhere = {};
        const finalWhere = Object.assign({}, baseWhere);
        const skip = lodash_1.default.max([0, (findAllBotDto.current - 1) * page_size]);
        return {
            current: findAllBotDto.current,
            pageSize: page_size,
            success: true,
            total: await this.prisma[entity_name].count(),
            data: await this.prisma[entity_name].findMany({
                where: finalWhere,
                skip,
                take: page_size
            })
        };
    }
};
BotService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [typeof (_a = typeof nestjs_prisma_1.PrismaService !== "undefined" && nestjs_prisma_1.PrismaService) === "function" ? _a : Object])
], BotService);
exports.BotService = BotService;


/***/ }),
/* 34 */
/***/ ((module) => {

module.exports = require("lodash");

/***/ }),
/* 35 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.CreateBotDto = void 0;
const class_validator_1 = __webpack_require__(36);
class CreateBotDto {
}
__decorate([
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateBotDto.prototype, "host", void 0);
__decorate([
    (0, class_validator_1.IsInt)(),
    __metadata("design:type", Number)
], CreateBotDto.prototype, "port", void 0);
__decorate([
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateBotDto.prototype, "desc", void 0);
exports.CreateBotDto = CreateBotDto;


/***/ }),
/* 36 */
/***/ ((module) => {

module.exports = require("class-validator");

/***/ }),
/* 37 */
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FindAllBotDto = void 0;
const class_validator_1 = __webpack_require__(36);
class FindAllBotDto {
}
__decorate([
    (0, class_validator_1.IsInt)(),
    __metadata("design:type", Number)
], FindAllBotDto.prototype, "current", void 0);
__decorate([
    (0, class_validator_1.IsString)(),
    __metadata("design:type", Number)
], FindAllBotDto.prototype, "pageSize", void 0);
exports.FindAllBotDto = FindAllBotDto;


/***/ }),
/* 38 */
/***/ ((module) => {

module.exports = require("path");

/***/ })
/******/ 	]);
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// This entry need to be wrapped in an IIFE because it need to be isolated against other modules in the chunk.
(() => {
var exports = __webpack_exports__;

Object.defineProperty(exports, "__esModule", ({ value: true }));
const core_1 = __webpack_require__(1);
const app_module_1 = __webpack_require__(2);
const config_1 = __webpack_require__(4);
const path_1 = __webpack_require__(38);
async function bootstrap() {
    const app = await core_1.NestFactory.create(app_module_1.AppModule);
    const configService = app.get(config_1.ConfigService);
    app.enableCors();
    app.setGlobalPrefix('mtxcms');
    const static_root = (0, path_1.join)(process.cwd(), 'public');
    app.useStaticAssets(static_root, {
        prefix: '/static/',
    });
    const port = configService.get('PORT') || 3000;
    await app.listen(port);
    console.log(`⚡️[mtxtun-v2] serve on port: ${port}, url: ${await app.getUrl()}`);
}
bootstrap();

})();

/******/ })()
;